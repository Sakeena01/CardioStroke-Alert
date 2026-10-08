from datetime import datetime
from zoneinfo import ZoneInfo

from models.user import db


# =========================================================
# INDIAN STANDARD TIME
# =========================================================

def indian_time():
    return datetime.now(ZoneInfo("Asia/Kolkata"))


# =========================================================
# PREDICTION HISTORY MODEL
# =========================================================

class PredictionHistory(db.Model):

    __tablename__ = "prediction_history"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        nullable=True
    )

    age = db.Column(
        db.Float
    )

    heart_rate = db.Column(
        db.Float
    )

    spo2 = db.Column(
        db.Float
    )

    glucose = db.Column(
        db.Float
    )

    bmi = db.Column(
        db.Float
    )

    systolic_bp = db.Column(
        db.Float
    )

    diastolic_bp = db.Column(
        db.Float
    )

    steps = db.Column(
        db.Float
    )

    prediction = db.Column(
        db.String(100)
    )

    confidence = db.Column(
        db.Float
    )

    stroke_probability = db.Column(
        db.Float
    )

    normal_probability = db.Column(
        db.Float
    )

    created_at = db.Column(
        db.DateTime,
        default=indian_time
    )