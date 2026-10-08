from app import app
from ml.thirty_day_risk import analyze_10_day_risk


with app.app_context():

    user_id = 1

    result = analyze_10_day_risk(user_id)

    print("\n========== 30 DAY HEALTH ANALYSIS ==========")

    for key, value in result.items():
        if key not in ["overall", "recent_7_days", "previous_period"]:
            print(f"{key}: {value}")

    print("\n---------- OVERALL 30 DAYS ----------")
    print(result.get("overall"))

    print("\n---------- RECENT 7 DAYS ----------")
    print(result.get("recent_7_days"))

    print("\n---------- PREVIOUS PERIOD ----------")
    print(result.get("previous_period"))

    print("\n============================================")