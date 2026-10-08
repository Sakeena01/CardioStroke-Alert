def calculate_health_score(
        heart_rate,
        spo2,
        bmi,
        glucose,
        steps):

    """
    Calculate an overall health score from 0 to 100.

    This is a project-level wellness score.
    It is not a medical diagnosis.
    """

    # ---------------------------------------------------------
    # Start with perfect score
    # ---------------------------------------------------------

    score = 100

    # ---------------------------------------------------------
    # Helper function
    # ---------------------------------------------------------

    def safe_float(value, default=None):

        try:

            if value is None:
                return default

            return float(value)

        except (TypeError, ValueError):

            return default

    # ---------------------------------------------------------
    # Convert values safely
    # ---------------------------------------------------------

    heart_rate = safe_float(heart_rate)
    spo2 = safe_float(spo2)
    bmi = safe_float(bmi)
    glucose = safe_float(glucose)
    steps = safe_float(steps)

    # ---------------------------------------------------------
    # SpO2
    # ---------------------------------------------------------

    if spo2 is not None:

        if spo2 < 90:

            score -= 25

        elif spo2 < 95:

            score -= 15

        elif spo2 < 97:

            score -= 5

    # ---------------------------------------------------------
    # Heart Rate
    # ---------------------------------------------------------

    if heart_rate is not None:

        if heart_rate > 120:

            score -= 20

        elif heart_rate > 110:

            score -= 15

        elif heart_rate < 50:

            score -= 10

        elif heart_rate < 60:

            score -= 5

    # ---------------------------------------------------------
    # BMI
    # ---------------------------------------------------------

    if bmi is not None and bmi > 0:

        if bmi < 18.5:

            score -= 10

        elif bmi > 30:

            score -= 10

        elif bmi >= 25:

            score -= 5

    # ---------------------------------------------------------
    # Blood Glucose
    # ---------------------------------------------------------

    if glucose is not None and glucose > 0:

        if glucose > 200:

            score -= 20

        elif glucose > 180:

            score -= 15

        elif glucose > 140:

            score -= 5

    # ---------------------------------------------------------
    # Daily Steps
    # ---------------------------------------------------------

    if steps is not None:

        if steps < 3000:

            score -= 10

        elif steps < 5000:

            score -= 5

    # ---------------------------------------------------------
    # Keep score between 0 and 100
    # ---------------------------------------------------------

    score = max(
        0,
        min(100, round(score))
    )

    return score


# =============================================================
# HEALTH SCORE CATEGORY
# =============================================================

def get_health_score_category(score):

    score = max(
        0,
        min(100, float(score))
    )

    if score >= 85:

        return "Excellent"

    elif score >= 70:

        return "Good"

    elif score >= 50:

        return "Needs Improvement"

    else:

        return "Poor"