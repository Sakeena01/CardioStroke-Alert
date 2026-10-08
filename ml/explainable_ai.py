from math import isnan


# ============================================================
# EXPLAINABLE AI
# ============================================================

FEATURE_NAMES = [
    "age",
    "heart_rate",
    "spo2",
    "sbp",
    "dbp",
    "bmi",
    "glucose",
    "steps"
]


DISPLAY_NAMES = {
    "age": "Age",
    "heart_rate": "Heart Rate",
    "spo2": "SpO₂",
    "sbp": "Systolic Blood Pressure",
    "dbp": "Diastolic Blood Pressure",
    "bmi": "BMI",
    "glucose": "Glucose",
    "steps": "Daily Steps"
}


def safe_number(value, default=0):

    try:

        value = float(value)

        if isnan(value):

            return default

        return value

    except Exception:

        return default


# ============================================================
# FEATURE CONDITION
# ============================================================

def get_feature_condition(
    feature,
    value
):

    value = safe_number(value)


    if feature == "age":

        if value >= 65:
            return "High"

        elif value >= 50:
            return "Moderate"

        else:
            return "Normal"


    if feature == "heart_rate":

        if value > 100 or value < 50:
            return "High"

        elif value > 90 or value < 60:
            return "Moderate"

        else:
            return "Normal"


    if feature == "spo2":

        if value < 94:
            return "High"

        elif value < 96:
            return "Moderate"

        else:
            return "Normal"


    if feature == "sbp":

        if value >= 140:
            return "High"

        elif value >= 130:
            return "Moderate"

        else:
            return "Normal"


    if feature == "dbp":

        if value >= 90:
            return "High"

        elif value >= 80:
            return "Moderate"

        else:
            return "Normal"


    if feature == "bmi":

        if value >= 30:
            return "High"

        elif value >= 25:
            return "Moderate"

        else:
            return "Normal"


    if feature == "glucose":

        if value >= 200:
            return "High"

        elif value >= 140:
            return "Moderate"

        else:
            return "Normal"


    if feature == "steps":

        if value < 3000:
            return "High"

        elif value < 5000:
            return "Moderate"

        else:
            return "Normal"


    return "Normal"


# ============================================================
# FEATURE EXPLANATION
# ============================================================

def explain_feature(
    feature,
    value
):

    value = safe_number(value)

    condition = get_feature_condition(
        feature,
        value
    )

    display_name = DISPLAY_NAMES.get(
        feature,
        feature
    )


    if condition == "High":

        severity = "High"

    elif condition == "Moderate":

        severity = "Moderate"

    else:

        severity = "Normal"


    return {

        "feature": feature,

        "name": display_name,

        "value": round(value, 2),

        "condition": condition,

        "severity": severity

    }


# ============================================================
# EXPLAIN PREDICTION
# ============================================================

def explain_prediction(
    age,
    heart_rate,
    spo2,
    sbp,
    dbp,
    bmi,
    glucose,
    steps,
    prediction,
    confidence
):

    values = {

        "age": age,

        "heart_rate": heart_rate,

        "spo2": spo2,

        "sbp": sbp,

        "dbp": dbp,

        "bmi": bmi,

        "glucose": glucose,

        "steps": steps

    }


    explanations = []


    for feature in FEATURE_NAMES:

        explanations.append(

            explain_feature(
                feature,
                values[feature]
            )

        )


    # ========================================================
    # SORT BY SEVERITY
    # ========================================================

    severity_order = {

        "High": 3,

        "Moderate": 2,

        "Normal": 1

    }


    explanations.sort(

        key=lambda item:
        severity_order.get(
            item["severity"],
            1
        ),

        reverse=True

    )


    # ========================================================
    # RISK FACTORS
    # ========================================================

    high_factors = [

        item
        for item in explanations
        if item["severity"] == "High"

    ]


    moderate_factors = [

        item
        for item in explanations
        if item["severity"] == "Moderate"

    ]


    normal_factors = [

        item
        for item in explanations
        if item["severity"] == "Normal"

    ]


    # ========================================================
    # SUMMARY
    # ========================================================

    if prediction == 1:

        summary = (
            "The model classified the current "
            "input as higher risk. The factors "
            "marked High or Moderate require "
            "attention."
        )

    else:

        summary = (
            "The model classified the current "
            "input as lower risk. Most monitored "
            "factors are within the project's "
            "defined normal ranges."
        )


    return {

        "prediction": prediction,

        "confidence": round(
            safe_number(confidence),
            2
        ),

        "summary": summary,

        "factors": explanations,

        "high_factors": high_factors,

        "moderate_factors": moderate_factors,

        "normal_factors": normal_factors,

        "high_count": len(high_factors),

        "moderate_count": len(moderate_factors),

        "normal_count": len(normal_factors)

    }