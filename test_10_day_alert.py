from app import app

from models.user import User
import ml.thirty_day_alert as alert_module


# ============================================================
# CONTROLLED 10-DAY HIGH-RISK EMAIL TEST
# ============================================================

def fake_10_day_analysis(user_id):

    return {
        "success": True,

        "risk": "High Risk",
        "risk_score": 7,

        "risk_factors": [
            "Low average SpO2",
            "Abnormal average heart rate"
        ],

        "overall_risk": "High Risk",
        "overall_risk_score": 7,

        "recent_risk": "High Risk",
        "recent_risk_score": 7,

        "previous_risk": "Moderate Risk",
        "previous_risk_score": 3,

        "trend": "Worsening",
        "trend_score": 4,
        "direction": "Risk is increasing",

        "days_observed": 10,
        "total_records": 100,

        "recent_records": 40,
        "previous_records": 60,

        "observation_status":
            "10-Day Observation Complete",

        "average_heart_rate": 105.5,
        "average_spo2": 92.8,
        "average_steps": 2100,
        "average_calories": 1200,
        "average_distance": 1.8,
        "average_sleep": 5.2,

        "valid_spo2_count": 95,
        "invalid_spo2_count": 5,

        "records": []
    }


# ============================================================
# TEMPORARILY REPLACE REAL ANALYSIS
# ============================================================

alert_module.analyze_30_day_risk = fake_10_day_analysis


# ============================================================
# RUN TEST
# ============================================================

with app.app_context():

    user = User.query.first()

    if not user:

        print()
        print("ERROR: No user found in database.")
        print()

    else:

        print()
        print("=" * 60)
        print("       CONTROLLED 10-DAY EMAIL ALERT TEST")
        print("=" * 60)

        print("User ID:", user.id)
        print("User Email:", user.email)

        print("-" * 60)

        result = alert_module.process_10_day_alert(
            app,
            user
        )

        print()
        print("-" * 60)
        print("TEST RESULT")
        print("-" * 60)

        print(
            "SUCCESS:",
            result.get("success")
        )

        print(
            "ALERT SENT:",
            result.get("alert_sent")
        )

        print(
            "MESSAGE:",
            result.get("message")
        )

        analysis = result.get(
            "analysis",
            {}
        )

        print(
            "RISK:",
            analysis.get("risk")
        )

        print(
            "RISK SCORE:",
            analysis.get("risk_score")
        )

        print(
            "DAYS:",
            analysis.get("days_observed")
        )

        print(
            "TREND:",
            analysis.get("trend")
        )

        print("=" * 60)
        print("       TEST COMPLETED")
        print("=" * 60)