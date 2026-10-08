import joblib
import pandas as pd


# =====================================================
# Load Wearable Model
# =====================================================

model = joblib.load(
    "models/wearable_model.pkl"
)

scaler = joblib.load(
    "models/wearable_scaler.pkl"
)


# =====================================================
# Feature Names
# =====================================================

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


# =====================================================
# Prediction Function
# =====================================================

def predict_health(data):

    # Convert input into DataFrame
    x = pd.DataFrame(
        [data],
        columns=FEATURES
    )

    # Apply scaler
    x_scaled = scaler.transform(x)

    # Prediction
    prediction = model.predict(x_scaled)[0]

    # Prediction probability
    probability = model.predict_proba(x_scaled)[0]

    confidence = round(
        max(probability) * 100,
        2
    )

    stroke_probability = round(
        probability[1] * 100,
        2
    )

    normal_probability = round(
        probability[0] * 100,
        2
    )

    return (
        int(prediction),
        confidence,
        stroke_probability,
        normal_probability
    )