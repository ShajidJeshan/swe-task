from flask import Flask, jsonify, request
from datetime import datetime, timedelta
from db import db, Reading
from utils import parse_data
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
db.init_app(app)
with app.app_context():
    db.create_all()


@app.route("/data/", methods=["POST"])
def post_data():
    """
    Store data in the database.

    Expects data in plaintext format, with each line representing a reading consisting of timestamp, metric name, and metric value.
    Returns a JSON response with success status.

    Example Request:
    POST /data
    Body:
    1649941817 Voltage 1.34
    1649941818 Voltage 1.35
    1649941817 Current 12.0
    1649941818 Current 14.0

    Example Response:
    {
        "success": true
    }
    """
    data = request.get_data(as_text=True)
    try:
        readings = parse_data(data)
        if readings:
            for reading in readings:
                load = Reading(timestamp=reading["timestamp"], name=reading["name"], value=reading["value"])
                db.session.add(load)
            db.session.commit()
            return jsonify({"success": True}), 200
        else:
            return jsonify({"success": False}), 400
    except ValueError:
        return jsonify({"success": False}), 400


@app.route("/data", methods=["GET"])
def get_data():
    """
    Retrieve data within the specified date range and calculate average power per day.

    URL: GET /data?from={from_date}&to={to_date}

    Parameters:
        - from_date (str): Start date in ISO format (YYYY-MM-DD).
        - to_date (str): End date in ISO format (YYYY-MM-DD).

    Returns:
        - JSON response with success status, data, and average power per day.

    Example Request:
        GET /data?from=2022-04-14&to=2022-04-15

    Example Response:
        {
            "success": true,
            "data": [
                {
                    "time": "2022-04-14T13:10:17.000Z",
                    "name": "Voltage",
                    "value": 1.34
                },
                {
                    "time": "2022-04-14T13:10:17.000Z",
                    "name": "Current",
                    "value": 12.0
                },
                ...
            ],
            "avg_power_per_day": [
                {
                    "date": "2022-04-14",
                    "average_power": 16.08
                },
                ...
            ]
        }
    """
    from_date = datetime.fromisoformat(request.args.get("from"))
    to_date = datetime.fromisoformat(request.args.get("to")) + timedelta(days=1)

    readings = (
        Reading.query
        .filter(Reading.timestamp.between(from_date, to_date))
        .all()
    )

    data = [
        {
            "time": reading.timestamp.isoformat(),
            "name": reading.name,
            "value": reading.value
        }
        for reading in readings
    ]

    average_power = {}

    for reading in readings:
        date = str(reading.timestamp.date())
        key = reading.name
        volt = int(key == "Voltage")
        current = int(key == "Current")

        average_power.setdefault(date, {}).setdefault(key, 0.0)
        average_power.setdefault(date, {}).setdefault("volt_count", 0)
        average_power.setdefault(date, {}).setdefault("current_count", 0)
        average_power[date][key] += round(reading.value, 2)
        average_power[date]["volt_count"] += volt
        average_power[date]["current_count"] += current

    avg_power_per_day = [
        {
            "date": key,
            "average_power": (average_power[key].get("Voltage", 0) / (1 if average_power[key].get("volt_count", 0) == 0 else average_power[key].get("volt_count", 0))) *
                             (average_power[key].get("Current", 0) / (1 if average_power[key].get("current_count", 0) == 0 else average_power[key].get("current_count", 0)))
        }
        for key in average_power
    ]

    return jsonify({"success": True, "data": data, "avg_power_per_day": avg_power_per_day}), 200


if __name__ == "__main__":
    app.run()
