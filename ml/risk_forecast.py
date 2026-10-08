def forecast(health_score):
    """
    Convert the health score into a simple risk category.
    Higher score = better health.
    """

    try:
        score = float(health_score)
    except (TypeError, ValueError):
        return "Unknown Risk"

    if score >= 80:
        return "Low Risk"

    elif score >= 60:
        return "Moderate Risk"

    else:
        return "High Risk"


def forecast_from_trend(
    current_score,
    previous_score=None,
    trend=None
):
    """
    Estimate the direction of health risk using
    current score, previous score and 10-day trend.
    """

    try:
        current_score = float(current_score)
    except (TypeError, ValueError):
        return {
            "risk": "Unknown Risk",
            "direction": "Insufficient Data",
            "score": 0
        }

    # ----------------------------------------------------
    # CURRENT RISK
    # ----------------------------------------------------

    current_risk = forecast(current_score)


    # ----------------------------------------------------
    # NO PREVIOUS DATA
    # ----------------------------------------------------

    if previous_score is None:

        return {
            "risk": current_risk,
            "direction": "Collecting data",
            "score": current_score
        }


    try:
        previous_score = float(previous_score)
    except (TypeError, ValueError):

        return {
            "risk": current_risk,
            "direction": "Insufficient Data",
            "score": current_score
        }


    # ----------------------------------------------------
    # SCORE CHANGE
    # ----------------------------------------------------

    change = round(
        current_score - previous_score,
        2
    )


    # ----------------------------------------------------
    # HEALTH DIRECTION
    # ----------------------------------------------------

    if trend == "Worsening" or change <= -5:

        direction = "Moving Toward High Risk"

    elif trend == "Improving" or change >= 5:

        direction = "Moving Toward Safe"

    else:

        direction = "Stable"


    # ----------------------------------------------------
    # RETURN RESULT
    # ----------------------------------------------------

    return {

        "risk": current_risk,

        "direction": direction,

        "score": current_score,

        "previous_score": previous_score,

        "score_change": change,

        "trend": trend or "Insufficient Data"

    }