# PowerX Python Engineering Task

For details of the task, see https://powerxai.notion.site/Software-Engineer-Python-805bcc8b246448a1b549b386b95548ab

This is a simple Flask-based API for storing and analyzing data readings. It allows users to store data in plaintext format and retrieve average power readings per day within a specified date range.

## Prerequisites

- Python 3.7+
- Flask
- Flask-SQLAlchemy
- dotenv

## Installation

1. Clone the repository:

```bash
git clone https://github.com/ShajidJeshan/swe-task.git
cd swe-task
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Create the SQLite database:

```bash
python main.py
```

## Usage

### Add Data

To add data, make a POST request to the `/data` endpoint with readings in plaintext format, where each line represents a reading consisting of timestamp, metric name, and metric value.

Example Request:

```bash
curl --request POST \
  --url http://localhost:5000/data \
  --header 'Content-Type: text/plain' \
  --data '1649941817 Voltage 1.34
1649941818 Voltage 1.35
1649941817 Current 12.0
1649941818 Current 14.0'
```

Example Response:

```json
{
  "success": true
}
```

### Get Data

To retrieve data and calculate average power per day, make a GET request to the `/data` endpoint with the `from` and `to` query parameters specifying the date range in ISO format (YYYY-MM-DD).

Example Request:

```bash
curl --request GET \
  --url 'http://localhost:5000/data?from=2022-04-14&to=2022-04-15'
```

Example Response:

```json
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
```
