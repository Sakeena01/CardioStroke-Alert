from datetime import datetime
from zoneinfo import ZoneInfo

from models.user import db


def indian_time():
    return datetime.now(ZoneInfo("Asia/Kolkata"))


class HealthAlert(db.Model):

    __tablename__ = "health_alerts"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        nullable=False
    )

    alert_type = db.Column(
        db.String(100),
        nullable=False
    )

    risk = db.Column(
        db.String(50),
        nullable=False
    )

    risk_score = db.Column(
        db.Integer,
        default=0
    )

    sent_at = db.Column(
        db.DateTime,
        default=indian_time
    )