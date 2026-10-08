from flask import Blueprint, render_template

from models.health_data import HealthData
from models.user import User

from ml.thirty_day_risk import analyze_10_day_risk
from ml.risk_forecast import forecast_from_trend


# ============================================================
# BLUEPRINT
# ============================================================

analytics_bp = Blueprint(
    "analytics",
    __name__
)


# ============================================================
# ANALYTICS PAGE
# ============================================================

@analytics_bp.route("/analytics")
def analytics():

    # ========================================================
    # GET USER
    # ========================================================

    user = User.query.first()


    # ========================================================
    # NO USER
    # ========================================================

    if user is None:

        return render_template(

            "analytics.html",

            user=None,

            result={
                "success": False,
                "message": "No user found."
            },

            records=[],

            dates=[],
            heart_rate=[],
            spo2=[],
            steps=[],
            calories=[],
            distance=[],
            sleep=[],

            risk_score=0,
            recent_risk_score=0,
            previous_risk_score=0,

            trend="Insufficient Data",
            direction="Collecting data",

            risk_forecast={
                "risk": "No Data",
                "direction": "Collecting data",
                "score": 0,
                "previous_score": None,
                "score_change": 0,
                "trend": "Insufficient Data"
            }

        )


    # ========================================================
    # 30-DAY RISK ANALYSIS
    # ========================================================

    try:

        result = analyze_10_day_risk(
            user.id
        )

    except Exception as e:

        print(
            "Analytics Risk Error:",
            e
        )

        result = {

            "success": False,

            "message":
                "Unable to calculate 10-day risk.",

            "error":
                str(e)

        }


    # ========================================================
    # GET HEALTH RECORDS
    # ========================================================

    records = (

        HealthData.query

        .filter(
            HealthData.user_id == user.id
        )

        .order_by(
            HealthData.created_at.asc()
        )

        .all()

    )


    # ========================================================
    # CHART ARRAYS
    # ========================================================

    dates = []

    heart_rate = []

    spo2 = []

    steps = []

    calories = []

    distance = []

    sleep = []


    for record in records:

        # ----------------------------------------------------
        # DATE
        # ----------------------------------------------------

        if record.created_at:

            dates.append(
                record.created_at.strftime(
                    "%d/%m %H:%M"
                )
            )

        else:

            dates.append("--")


        # ----------------------------------------------------
        # HEART RATE
        # ----------------------------------------------------

        heart_rate.append(
            record.heart_rate
            if record.heart_rate is not None
            else None
        )


        # ----------------------------------------------------
        # SPO2
        # ----------------------------------------------------

        spo2.append(
            record.spo2
            if record.spo2 is not None
            else None
        )


        # ----------------------------------------------------
        # STEPS
        # ----------------------------------------------------

        steps.append(
            record.steps
            if record.steps is not None
            else None
        )


        # ----------------------------------------------------
        # CALORIES
        # ----------------------------------------------------

        calories.append(
            record.calories
            if record.calories is not None
            else None
        )


        # ----------------------------------------------------
        # DISTANCE
        # ----------------------------------------------------

        distance.append(
            record.distance
            if record.distance is not None
            else None
        )


        # ----------------------------------------------------
        # SLEEP
        # ----------------------------------------------------

        sleep.append(
            record.sleep
            if record.sleep is not None
            else None
        )


    # ========================================================
    # DEFAULT RISK VALUES
    # ========================================================

    risk_score = 0

    recent_risk_score = 0

    previous_risk_score = 0

    trend = "Insufficient Data"

    direction = "Collecting data"


    # ========================================================
    # GET RISK VALUES
    # ========================================================

    if result.get("success"):

        risk_score = result.get(
            "risk_score",
            0
        )

        recent_risk_score = result.get(
            "recent_risk_score",
            0
        )

        previous_risk_score = result.get(
            "previous_risk_score",
            0
        )

        trend = result.get(
            "trend",
            "Insufficient Data"
        )

        direction = result.get(
            "direction",
            "Collecting data"
        )


    # ========================================================
    # RISK FORECAST
    # ========================================================

    risk_forecast = {

        "risk": "No Data",

        "direction": "Collecting data",

        "score": 0,

        "previous_score": None,

        "score_change": 0,

        "trend": "Insufficient Data"

    }


    try:

        if result.get("success"):

            current_score = result.get(
                "risk_score",
                0
            )

            previous_score = result.get(
                "previous_risk_score"
            )

            trend_value = result.get(
                "trend",
                "Insufficient Data"
            )


            risk_forecast = forecast_from_trend(

                current_score=current_score,

                previous_score=previous_score,

                trend=trend_value

            )


    except Exception as e:

        print(
            "Risk Forecast Error:",
            e
        )


    # ========================================================
    # RENDER ANALYTICS
    # ========================================================

    return render_template(

        "analytics.html",

        user=user,

        result=result,

        records=records,

        dates=dates,

        heart_rate=heart_rate,

        spo2=spo2,

        steps=steps,

        calories=calories,

        distance=distance,

        sleep=sleep,

        risk_score=risk_score,

        recent_risk_score=recent_risk_score,

        previous_risk_score=previous_risk_score,

        trend=trend,

        direction=direction,

        risk_forecast=risk_forecast

    )