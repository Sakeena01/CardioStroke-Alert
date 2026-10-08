import joblib
import pandas as pd


# ============================================================
# LOAD WEARABLE MODEL
# ============================================================

model = joblib.load("models/wearable_model.pkl")
scaler = joblib.load("models/wearable_scaler.pkl")


# ============================================================
# FEATURE ORDER
# ============================================================

FEATURES = [
    "age",
    "heart_rate",
    "spo2",
    "sbp",
    "dbp",
    "bmi",
    "glucose",
    "steps"
]


# ============================================================
# WEARABLE PREDICTION
# ============================================================

def predict_wearable(data):

    # Create DataFrame with the same feature names
    # used during training.
    x = pd.DataFrame(
        [data],
        columns=FEATURES
    )

    # Apply the same scaler used during training
    x_scaled = scaler.transform(x)

    # Model prediction
    prediction = model.predict(x_scaled)[0]

    # Prediction probabilities
    probability = model.predict_proba(x_scaled)[0]

    # Confidence
    confidence = round(
        float(max(probability)) * 100,
        2
    )

    # Stroke probability
    stroke_probability = round(
        float(probability[1]) * 100,
        2
    )

    # Normal probability
    normal_probability = round(
        float(probability[0]) * 100,
        2
    )

    return {
        "prediction": int(prediction),
        "confidence": confidence,
        "stroke_probability": stroke_probability,
        "normal_probability": normal_probability
    }