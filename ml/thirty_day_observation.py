from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from models.health_data import HealthData


IST = ZoneInfo("Asia/Kolkata")

OBSERVATION_DAYS = 10


def average(values):
    if not values:
        return None

    return round(sum(values) / len(values), 2)


def valid_spo2(value):
    if value is None:
        return False

    try:
        value = float(value)
    except (TypeError, ValueError):
        return False

    return 70 <= value <= 100


def valid_heart_rate(value):
    if value is None:
        return False

    try:
        value = float(value)
    except (TypeError, ValueError):
        return False

    return value > 0


def valid_steps(value):
    if value is None:
        return False

    try:
        value = float(value)
    except (TypeError, ValueError):
        return False

    return value >= 0


def calculate_averages(records):

    heart_rate_values = [
        float(r.heart_rate)
        for r in records
        if valid_heart_rate(r.heart_rate)
    ]

    spo2_values = [
        float(r.spo2)
        for r in records
        if valid_spo2(r.spo2)
    ]

    steps_values = [
        float(r.steps)
        for r in records
        if valid_steps(r.steps)
    ]

    calories_values = [
        float(r.calories)
        for r in records
        if r.calories is not None
    ]

    distance_values = [
        float(r.distance)
        for r in records
        if r.distance is not None
    ]

    sleep_values = [
        float(r.sleep)
        for r in records
        if r.sleep is not None
    ]

    return {
        "heart_rate": average(heart_rate_values),
        "spo2": average(spo2_values),
        "steps": average(steps_values),
        "calories": average(calories_values),
        "distance": average(distance_values),
        "sleep": average(sleep_values)
    }


def get_30_day_observation(user_id):

    end_time = datetime.now(IST).replace(tzinfo=None)

    start_time = (
        end_time -
        timedelta(days=OBSERVATION_DAYS)
    )

    records = (
        HealthData.query
        .filter(
            HealthData.user_id == user_id,
            HealthData.created_at >= start_time,
            HealthData.created_at <= end_time
        )
        .order_by(
            HealthData.created_at.asc()
        )
        .all()
    )

    if not records:

        return {
            "days_observed": 0,
            "total_records": 0,
            "overall": {},
            "recent_7_days": {},
            "previous_period": {},
            "recent_records": 0,
            "previous_records": 0,
            "records": []
        }

    recent_start = (
        end_time -
        timedelta(days=7)
    )

    recent_records = [
        r
        for r in records
        if r.created_at
        and r.created_at >= recent_start
    ]

    previous_records = [
        r
        for r in records
        if r.created_at
        and r.created_at < recent_start
    ]

    overall = calculate_averages(records)

    recent_7_days = calculate_averages(
        recent_records
    )

    previous_period = calculate_averages(
        previous_records
    )

    observed_dates = set(
        r.created_at.date()
        for r in records
        if r.created_at is not None
    )

    days_observed = len(observed_dates)

    valid_spo2_count = sum(
        1
        for r in records
        if valid_spo2(r.spo2)
    )

    invalid_spo2_count = sum(
        1
        for r in records
        if (
            r.spo2 is not None
            and not valid_spo2(r.spo2)
        )
    )

    return {

        "days_observed": days_observed,

        "total_records": len(records),

        "observation_days":
            OBSERVATION_DAYS,

        "average_heart_rate":
            overall["heart_rate"],

        "average_spo2":
            overall["spo2"],

        "average_steps":
            overall["steps"],

        "average_calories":
            overall["calories"],

        "average_distance":
            overall["distance"],

        "average_sleep":
            overall["sleep"],

        "overall":
            overall,

        "recent_7_days":
            recent_7_days,

        "previous_period":
            previous_period,

        "recent_records":
            len(recent_records),

        "previous_records":
            len(previous_records),

        "valid_spo2_count":
            valid_spo2_count,

        "invalid_spo2_count":
            invalid_spo2_count,

        "records":
            records
    }