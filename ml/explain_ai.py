import numpy as np

def explain_prediction(
        heart_rate,
        spo2,
        sbp,
        dbp,
        glucose,
        bmi,
        steps):

    scores = {}

    if heart_rate > 100:
        scores["Heart Rate"] = 25

    if spo2 < 95:
        scores["SpO₂"] = 20

    if sbp > 140:
        scores["Blood Pressure"] = 25

    if glucose > 140:
        scores["Glucose"] = 20

    if bmi > 30:
        scores["BMI"] = 15

    if steps < 4000:
        scores["Physical Activity"] = 10

    if len(scores) == 0:
        scores["Healthy Lifestyle"] = 100

    return scores