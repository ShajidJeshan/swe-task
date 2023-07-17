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


@app.route("/data", methods=["POST"])
def post_data():
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


@app.get("/data")
def get_data():
    # TODO: check what dates have been requested, and retrieve all data within the given range

    return {"success": False}


if __name__ == "__main__":
    app.run()
