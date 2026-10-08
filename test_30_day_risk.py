from app import app
from ml.thirty_day_risk import analyze_10_day_risk


# =========================================================
# USER TO TEST
# =========================================================

USER_ID = 1


# =========================================================
# RUN INSIDE FLASK APPLICATION CONTEXT
# =========================================================

with app.app_context():

    print("======================================")
    print("10-DAY RISK ANALYSIS TEST")
    print("======================================")

    result = analyze_10_day_risk(USER_ID)

    print("Success:", result.get("success"))

    print("Risk:",
          result.get("risk"))

    print("Risk Score:",
          result.get("risk_score"))

    print("Days Observed:",
          result.get("days_observed"))

    print("Total Records:",
          result.get("total_records"))

    print("Observation Status:",
          result.get("observation_status"))

    print("--------------------------------------")

    print("Average Heart Rate:",
          result.get("average_heart_rate"))

    print("Average SpO2:",
          result.get("average_spo2"))

    print("Average Steps:",
          result.get("average_steps"))

    print("Average Sleep:",
          result.get("average_sleep"))

    print("--------------------------------------")

    print("Risk Factors:")

    for factor in result.get("risk_factors", []):

        print("-", factor)

    print("======================================")