from app import app
from models.health_data import HealthData
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo


with app.app_context():

    now = datetime.now(
        ZoneInfo("Asia/Kolkata")
    ).replace(tzinfo=None)

    seven_days_ago = now - timedelta(days=7)

    print("\n========== DATE DIAGNOSTIC ==========")

    print("Current IST :", now)
    print("7 Days Ago  :", seven_days_ago)

    records = (
        HealthData.query
        .filter(HealthData.user_id == 1)
        .order_by(HealthData.created_at.asc())
        .all()
    )

    print("\n---------- DATABASE RECORDS ----------")

    for record in records:

        if record.created_at >= seven_days_ago:
            period = "RECENT 7 DAYS"
        else:
            period = "PREVIOUS PERIOD"

        print(
            f"ID: {record.id} | "
            f"Time: {record.created_at} | "
            f"Period: {period}"
        )

    print("\n======================================")