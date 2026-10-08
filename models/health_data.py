from models.user import db
from datetime import datetime
from zoneinfo import ZoneInfo


def indian_time():
    return datetime.now(
        ZoneInfo("Asia/Kolkata")
    ).replace(tzinfo=None)


class HealthData(db.Model):

    __tablename__ = "health_data"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        nullable=True
    )

    # =====================================================
    # PRIMARY HEALTH DATA
    # =====================================================

    heart_rate = db.Column(
        db.Float
    )

    spo2 = db.Column(
        db.Float
    )

    # =====================================================
    # BLOOD PRESSURE
    # =====================================================

    systolic_bp = db.Column(
        db.Float
    )

    diastolic_bp = db.Column(
        db.Float
    )

    # =====================================================
    # GLUCOSE
    # =====================================================

    blood_glucose = db.Column(
        db.Float
    )

    # =====================================================
    # ACTIVITY
    # =====================================================

    steps = db.Column(
        db.Integer
    )

    calories = db.Column(
        db.Float
    )

    distance = db.Column(
        db.Float
    )

    # =====================================================
    # SLEEP
    # =====================================================

    sleep = db.Column(
        db.Float
    )

    # =====================================================
    # METADATA
    # =====================================================

    created_at = db.Column(
        db.DateTime,
        default=indian_time
    )

    source = db.Column(
        db.String(100),
        default="Health Connect"
    )

    device_name = db.Column(
        db.String(100),
        default="Unknown"
    )