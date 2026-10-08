def explain(age,
            heart_rate,
            spo2,
            bmi,
            glucose):

    reasons = []

    if age > 60:
        reasons.append("Higher age")

    if heart_rate > 110:
        reasons.append("High heart rate")

    if spo2 < 95:
        reasons.append("Low oxygen level")

    if bmi > 30:
        reasons.append("High BMI")

    if glucose > 180:
        reasons.append("High glucose")

    return reasons