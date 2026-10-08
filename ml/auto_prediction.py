import numpy as np

from ml.predictor import predict_health
from ml.health_score import calculate_health_score
from ml.recommendation import recommendation
from ml.risk_forecast import forecast


def run_automatic_prediction(
    age,
    heart_rate,
    spo2,
    sbp,
    dbp,
    bmi,
    glucose,
    steps,
    ecg,
    fall
):
    """
    Runs the existing XGBoost model using the same
    feature order as the manual prediction system.
    """

    # ---------------------------------------------------------
    # Prepare features in the EXACT order expected by model
    # ---------------------------------------------------------

    model_input = np.array([
        age,
        heart_rate,
        spo2,
        sbp,
        dbp,
        bmi,
        glucose,
        steps,
        ecg,
        fall
    ], dtype=float)

    # ---------------------------------------------------------
    # XGBoost prediction
    # ---------------------------------------------------------

    (
        prediction,
        confidence,
        stroke_probability,
        normal_probability
    ) = predict_health(model_input)

    # ---------------------------------------------------------
    # Health score
    # ---------------------------------------------------------

    health_score = calculate_health_score(
        heart_rate,
        spo2,
        bmi,
        glucose,
        steps
    )

    # ---------------------------------------------------------
    # Risk
    # ---------------------------------------------------------

    risk = forecast(health_score)

    # ---------------------------------------------------------
    # Recommendation
    # ---------------------------------------------------------

    tips = recommendation(health_score)

    # ---------------------------------------------------------
    # Return complete result
    # ---------------------------------------------------------

    return {
        "prediction": int(prediction),
        "confidence": float(confidence),
        "stroke_probability": float(stroke_probability),
        "normal_probability": float(normal_probability),
        "health_score": float(health_score),
        "risk": risk,
        "recommendation": tips
    }