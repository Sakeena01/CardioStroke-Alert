from flask import Blueprint, render_template

from models.health_data import HealthData
from models.prediction_history import PredictionHistory
from models.user import User

from ml.health_score import calculate_health_score
from ml.thirty_day_risk import analyze_10_day_risk
from ml.risk_forecast import forecast_from_trend
from ml.explainable_ai import explain_prediction


# ==========================================================
# BLUEPRINT
# ==========================================================

dashboard_bp = Blueprint(
    "dashboard",
    __name__
)


# ==========================================================
# DASHBOARD
# ==========================================================

@dashboard_bp.route("/dashboard")
def dashboard():

    # ======================================================
    # GET USER
    # ======================================================

    user = User.query.first()


    # ======================================================
    # DEFAULT VALUES
    # ======================================================

    latest = None

    latest_prediction = None

    health_score = 0

    prediction = "No Prediction"

    risk = "No Data"

    confidence = 0

    stroke_probability = 0

    normal_probability = 0

    automatic_result = None

    explanation_data = None


    # ======================================================
    # DEFAULT RISK FORECAST
    # ======================================================

    risk_forecast = {

        "forecast": "No Data",

        "direction": "Collecting data",

        "change": 0,

        "current_score": 0,

        "previous_score": 0
    }


    # ======================================================
    # DEFAULT 30-DAY RESULT
    # ======================================================

    thirty_day_result = {

        "success": False,

        "risk": "No Data",

        "risk_score": 0,

        "overall_risk": "No Data",

        "overall_risk_score": 0,

        "recent_risk": "No Data",

        "recent_risk_score": 0,

        "previous_risk": "No Data",

        "previous_risk_score": 0,

        "trend": "Insufficient Data",

        "trend_score": 0,

        "direction": "Collecting data",

        "days_observed": 0,

        "total_records": 0,

        "recent_records": 0,

        "previous_records": 0,

        "observation_status": "No Data",

        "average_heart_rate": None,

        "average_spo2": None,

        "average_steps": None,

        "average_sleep": None,

        "risk_factors": [],

        "overall": {},

        "recent_7_days": {},

        "previous_period": {}

    }


    # ======================================================
    # GET USER DATA
    # ======================================================

    if user:

        # ==================================================
        # LATEST HEALTH RECORD
        # ==================================================

        latest = (

            HealthData.query

            .filter(
                HealthData.user_id == user.id
            )

            .order_by(
                HealthData.created_at.desc()
            )

            .first()

        )


        # ==================================================
        # LATEST SAVED PREDICTION
        # ==================================================

        latest_prediction = (

            PredictionHistory.query

            .filter(
                PredictionHistory.user_id == user.id
            )

            .order_by(
                PredictionHistory.created_at.desc()
            )

            .first()

        )


    # ======================================================
    # HEALTH SCORE
    # ======================================================

    if latest and user:

        try:

            health_score = calculate_health_score(

                latest.heart_rate or 0,

                latest.spo2 or 0,

                user.bmi or 0,

                user.glucose or 0,

                latest.steps or 0

            )

        except Exception as e:

            print(
                "Health Score Error:",
                e
            )

            health_score = 0


    # ======================================================
    # USE LATEST SAVED XGBOOST PREDICTION
    # ======================================================

    if latest_prediction:

        # ==================================================
        # PREDICTION
        # ==================================================

        prediction = latest_prediction.prediction


        # ==================================================
        # RISK
        # ==================================================

        if prediction:

            if "High" in str(prediction):

                risk = "High Risk"

            elif "Low" in str(prediction):

                risk = "Low Risk"

            else:

                risk = str(prediction)


        # ==================================================
        # CONFIDENCE
        # ==================================================

        confidence = (

            float(
                latest_prediction.confidence
            )

            if latest_prediction.confidence is not None

            else 0

        )


        # ==================================================
        # STROKE PROBABILITY
        # ==================================================

        stroke_probability = (

            float(
                latest_prediction.stroke_probability
            )

            if latest_prediction.stroke_probability is not None

            else 0

        )


        # ==================================================
        # NORMAL PROBABILITY
        # ==================================================

        normal_probability = (

            float(
                latest_prediction.normal_probability
            )

            if latest_prediction.normal_probability is not None

            else 0

        )


        # ==================================================
        # AUTOMATIC RESULT
        # ==================================================

        automatic_result = {

            "success": True,

            "prediction":
                prediction,

            "risk":
                risk,

            "confidence":
                confidence,

            "stroke_probability":
                stroke_probability,

            "normal_probability":
                normal_probability,

            "history_id":
                latest_prediction.id,

            "age":
                latest_prediction.age,

            "heart_rate":
                latest_prediction.heart_rate,

            "spo2":
                latest_prediction.spo2,

            "systolic_bp":
                latest_prediction.systolic_bp,

            "diastolic_bp":
                latest_prediction.diastolic_bp,

            "bmi":
                latest_prediction.bmi,

            "glucose":
                latest_prediction.glucose,

            "steps":
                latest_prediction.steps

        }


        # ==================================================
        # EXPLAINABLE AI
        # ==================================================

        try:

            xai_prediction = (

                1

                if "High" in str(prediction)

                else 0

            )


            explanation_data = explain_prediction(

                age=latest_prediction.age,

                heart_rate=latest_prediction.heart_rate,

                spo2=latest_prediction.spo2,

                sbp=latest_prediction.systolic_bp,

                dbp=latest_prediction.diastolic_bp,

                bmi=latest_prediction.bmi,

                glucose=latest_prediction.glucose,

                steps=latest_prediction.steps,

                prediction=xai_prediction,

                confidence=confidence

            )


            automatic_result[
                "explanation"
            ] = explanation_data


        except Exception as e:

            print(
                "Dashboard XAI Error:",
                e
            )

            explanation_data = None


    # ======================================================
    # NO PREDICTION YET
    # ======================================================

    else:

        automatic_result = {

            "success": False,

            "prediction": None,

            "risk": "No Prediction",

            "confidence": 0,

            "stroke_probability": 0,

            "normal_probability": 0,

            "message":
                "Synchronize health data to generate an automatic prediction."

        }


    # ======================================================
    # 30-DAY RISK ANALYSIS
    # ======================================================

    if user:

        try:

            thirty_day_result = (

                analyze_10_day_risk(

                    user.id

                )

            )

        except Exception as e:

            print(
                "10-Day Dashboard Analysis Error:",
                e
            )


    # ======================================================
    # RISK FORECAST
    # ======================================================

    try:

        current_score = float(

            thirty_day_result.get(
                "recent_risk_score",
                0
            )

        )


        previous_score = float(

            thirty_day_result.get(
                "previous_risk_score",
                0
            )

        )


        trend = thirty_day_result.get(

            "trend",

            "Insufficient Data"

        )


        risk_forecast = forecast_from_trend(

            current_score=current_score,

            previous_score=previous_score,

            trend=trend

        )

        if not isinstance(
            risk_forecast,
            dict
        ):

            risk_forecast = {

                "forecast":
                    str(risk_forecast),

                "direction":
                    "Stable",

                "change":
                    current_score - previous_score,

                "current_score":
                    current_score,

                "previous_score":
                    previous_score

            }


    except Exception as e:

        print(
            "Risk Forecast Error:",
            e
        )


        risk_forecast = {

            "forecast": "No Data",

            "direction":
                "Collecting data",

            "change": 0,

            "current_score": 0,

            "previous_score": 0

        }


    # ======================================================
    # HEALTH CHART DATA
    # ======================================================

    dates = []

    heart_rate = []

    spo2 = []

    steps = []

    calories = []


    if user:

        records = (

            HealthData.query

            .filter(
                HealthData.user_id == user.id
            )

            .order_by(
                HealthData.created_at.asc()
            )

            .limit(30)

            .all()

        )


        for record in records:

            if record.created_at:

                dates.append(

                    record.created_at.strftime(
                        "%d/%m %H:%M"
                    )

                )

            else:

                dates.append("")


            heart_rate.append(

                record.heart_rate or 0

            )


            spo2.append(

                record.spo2 or 0

            )


            steps.append(

                record.steps or 0

            )


            calories.append(

                record.calories or 0

            )


    # ======================================================
    # RENDER DASHBOARD
    # ======================================================

    return render_template(

        "dashboard.html",

        # --------------------------------------------------
        # USER / HEALTH
        # --------------------------------------------------

        user=user,

        latest=latest,

        health_score=health_score,


        # --------------------------------------------------
        # PREDICTION
        # --------------------------------------------------

        prediction=prediction,

        risk=risk,

        confidence=confidence,

        stroke_probability=stroke_probability,

        normal_probability=normal_probability,

        automatic_result=automatic_result,

        latest_prediction=latest_prediction,


        # --------------------------------------------------
        # XAI
        # --------------------------------------------------

        explanation_data=explanation_data,


        # --------------------------------------------------
        # RISK FORECAST
        # --------------------------------------------------

        risk_forecast=risk_forecast,


        # --------------------------------------------------
        # CHART DATA
        # --------------------------------------------------

        dates=dates,

        heart_rate=heart_rate,

        spo2=spo2,

        steps=steps,

        calories=calories,


        # --------------------------------------------------
        # 30-DAY ANALYSIS
        # --------------------------------------------------

        thirty_day_result=thirty_day_result
    )