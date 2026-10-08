from app import app
from models.user import User
from ml.thirty_day_observation import get_10_day_observation
from ml.thirty_day_risk import analyze_10_day_risk


def print_section(title):
    print()
    print("=" * 60)
    print(title)
    print("=" * 60)


with app.app_context():

    # ==========================================================
    # USER
    # ==========================================================

    user = User.query.first()

    if not user:
        print("ERROR: No user found in database.")
        raise SystemExit

    print_section("10-DAY HEALTH OBSERVATION TEST")

    print("User ID:", user.id)

    # ==========================================================
    # OBSERVATION
    # ==========================================================

    observation = get_10_day_observation(user.id)

    print_section("OBSERVATION SUMMARY")

    print("Days Observed:",
          observation.get("days_observed", 0), "/ 30")

    print("Total Records:",
          observation.get("total_records", 0))

    print("Recent 7-Day Records:",
          observation.get("recent_records", 0))

    print("Previous Period Records:",
          observation.get("previous_records", 0))

    print()

    print("Average Heart Rate:",
          observation.get("average_heart_rate"))

    print("Average SpO2:",
          observation.get("average_spo2"))

    print("Average Steps:",
          observation.get("average_steps"))

    print("Average Calories:",
          observation.get("average_calories"))

    print("Average Distance:",
          observation.get("average_distance"))

    print("Average Sleep:",
          observation.get("average_sleep"))

    # ==========================================================
    # RISK ANALYSIS
    # ==========================================================

    result = analyze_10_day_risk(user.id)

    print_section("10-DAY RISK ANALYSIS")

    print("Success:",
          result.get("success"))

    print("Observation Status:",
          result.get("observation_status"))

    print()

    print("Current Risk:",
          result.get("risk"))

    print("Current Risk Score:",
          result.get("risk_score"))

    print()

    print("Overall Risk:",
          result.get("overall_risk"))

    print("Overall Risk Score:",
          result.get("overall_risk_score"))

    print()

    print("Recent 7-Day Risk:",
          result.get("recent_risk"))

    print("Recent 7-Day Score:",
          result.get("recent_risk_score"))

    print()

    print("Previous Period Risk:",
          result.get("previous_risk"))

    print("Previous Period Score:",
          result.get("previous_risk_score"))

    # ==========================================================
    # TREND
    # ==========================================================

    print_section("HEALTH TREND")

    print("Trend:",
          result.get("trend"))

    print("Direction:",
          result.get("direction"))

    print("Trend Score:",
          result.get("trend_score"))

    # ==========================================================
    # RISK FACTORS
    # ==========================================================

    print_section("RISK FACTORS")

    factors = result.get("risk_factors", [])

    if factors:
        for factor in factors:
            print("-", factor)
    else:
        print("No significant risk factors detected.")

    # ==========================================================
    # FINAL
    # ==========================================================

    print_section("10-DAY TEST COMPLETED")

    print("The database was only read.")
    print("No health records were modified.")
    print("No prediction records were modified.")