from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()


class Reading(db.Model):
    __tablename__ = 'reading'
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, nullable=False)
    name = db.Column(db.String(50), nullable=False)
    value = db.Column(db.Float, nullable=False)

    def __init__(self, timestamp, name, value):
        self.timestamp = timestamp
        self.name = name
        self.value = value
