from ml.thirty_day_observation import (
    get_30_day_observation
)


def calculate_risk_score(metrics):

    score = 0

    factors = []

    heart_rate = metrics.get(
        "heart_rate"
    )

    spo2 = metrics.get(
        "spo2"
    )

    steps = metrics.get(
        "steps"
    )

    sleep = metrics.get(
        "sleep"
    )

    if heart_rate is not None:

        if (
            heart_rate > 100
            or heart_rate < 50
        ):

            score += 2

            factors.append(
                "Abnormal average heart rate"
            )

    if spo2 is not None:

        if spo2 < 94:

            score += 3

            factors.append(
                "Low average SpO2"
            )

        elif spo2 < 96:

            score += 1

            factors.append(
                "Borderline average SpO2"
            )

    if steps is not None:

        if steps < 3000:

            score += 2

            factors.append(
                "Low average daily steps"
            )

        elif steps < 5000:

            score += 1

            factors.append(
                "Below recommended daily steps"
            )

    if sleep is not None:

        if sleep < 5:

            score += 2

            factors.append(
                "Low average sleep"
            )

        elif sleep < 7:

            score += 1

            factors.append(
                "Below recommended sleep"
            )

    if score >= 5:

        risk = "High Risk"

    elif score >= 3:

        risk = "Moderate Risk"

    else:

        risk = "Low Risk"

    return risk, score, factors


def analyze_10_day_risk(user_id):

    observation = (
        get_30_day_observation(user_id)
    )

    if not observation:

        return {
            "success": False,
            "risk": "No Data",
            "risk_score": 0,
            "risk_factors": [],
            "days_observed": 0,
            "total_records": 0,
            "observation_status": "No Data"
        }

    days_observed = observation.get(
        "days_observed",
        0
    )

    total_records = observation.get(
        "total_records",
        0
    )

    overall = observation.get(
        "overall",
        {}
    )

    recent = observation.get(
        "recent_7_days",
        {}
    )

    previous = observation.get(
        "previous_period",
        {}
    )

    overall_risk, overall_score, overall_factors = (
        calculate_risk_score(overall)
    )

    recent_risk, recent_score, recent_factors = (
        calculate_risk_score(recent)
    )

    previous_risk, previous_score, previous_factors = (
        calculate_risk_score(previous)
    )

    difference = (
        recent_score -
        previous_score
    )

    if (
        previous_score == 0
        and recent_score == 0
    ):

        trend = "Stable"

        direction = "Risk is stable"

    elif difference >= 2:

        trend = "Worsening"

        direction = "Risk is increasing"

    elif difference <= -2:

        trend = "Improving"

        direction = "Risk is decreasing"

    else:

        trend = "Stable"

        direction = "Risk is stable"

    if recent:

        current_risk = recent_risk
        current_score = recent_score
        current_factors = recent_factors

    else:

        current_risk = overall_risk
        current_score = overall_score
        current_factors = overall_factors

    # ==========================================
    # 10-DAY OBSERVATION STATUS
    # ==========================================

    if days_observed < 10:

        observation_status = (
            f"Collecting data "
            f"({days_observed}/10 days)"
        )

        trend = "Insufficient Data"

        direction = "Collecting data"

    else:

        observation_status = (
            "10-Day Observation Complete"
        )

    return {

        "success": True,

        "risk":
            current_risk,

        "risk_score":
            current_score,

        "risk_factors":
            current_factors,

        "overall_risk":
            overall_risk,

        "overall_risk_score":
            overall_score,

        "overall_risk_factors":
            overall_factors,

        "recent_risk":
            recent_risk,

        "recent_risk_score":
            recent_score,

        "recent_risk_factors":
            recent_factors,

        "previous_risk":
            previous_risk,

        "previous_risk_score":
            previous_score,

        "previous_risk_factors":
            previous_factors,

        "trend":
            trend,

        "trend_score":
            difference,

        "direction":
            direction,

        "days_observed":
            days_observed,

        "observation_days":
            10,

        "total_records":
            total_records,

        "recent_records":
            observation.get(
                "recent_records",
                0
            ),

        "previous_records":
            observation.get(
                "previous_records",
                0
            ),

        "observation_status":
            observation_status,

        "average_heart_rate":
            observation.get(
                "average_heart_rate"
            ),

        "average_spo2":
            observation.get(
                "average_spo2"
            ),

        "average_steps":
            observation.get(
                "average_steps"
            ),

        "average_calories":
            observation.get(
                "average_calories"
            ),

        "average_distance":
            observation.get(
                "average_distance"
            ),

        "average_sleep":
            observation.get(
                "average_sleep"
            ),

        "overall":
            overall,

        "recent_7_days":
            recent,

        "previous_period":
            previous,

        "valid_spo2_count":
            observation.get(
                "valid_spo2_count",
                0
            ),

        "invalid_spo2_count":
            observation.get(
                "invalid_spo2_count",
                0
            ),

        "records":
            observation.get(
                "records",
                []
            )
    }