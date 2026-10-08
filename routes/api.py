from flask import Blueprint, jsonify

from models.health_data import HealthData
from models.prediction_history import PredictionHistory


api_bp = Blueprint("api", __name__)


# =========================================================
# LATEST PREDICTION
# =========================================================

@api_bp.route("/api/latest")
def latest_prediction():

    latest = (
        PredictionHistory.query
        .order_by(
            PredictionHistory.created_at.desc()
        )
        .first()
    )

    if latest is None:

        return jsonify({
            "status": "success",
            "heart_rate": 0,
            "spo2": 0,
            "steps": 0,
            "glucose": 0,
            "bmi": 0,
            "prediction": "No Data",
            "confidence": 0
        })


    return jsonify({

        "status": "success",

        "heart_rate":
            latest.heart_rate,

        "spo2":
            latest.spo2,

        "steps":
            latest.steps,

        "glucose":
            latest.glucose,

        "bmi":
            latest.bmi,

        "prediction":
            latest.prediction,

        "confidence":
            latest.confidence

    })


# =========================================================
# DASHBOARD / ANALYTICS DATA
# =========================================================

@api_bp.route("/api/dashboard_data")
def dashboard_data():

    try:

        # =================================================
        # HEALTH DATA
        # =================================================

        health_records = (
            HealthData.query
            .order_by(
                HealthData.created_at.asc()
            )
            .all()
        )


        # Keep latest 20 readings
        health_records = health_records[-20:]


        dates = [
            record.created_at.strftime(
                "%d/%m %H:%M"
            )
            for record in health_records
        ]


        heart_rate = [
            record.heart_rate
            for record in health_records
        ]


        spo2 = [
            record.spo2
            for record in health_records
        ]


        steps = [
            record.steps
            for record in health_records
        ]


        calories = [
            record.calories
            for record in health_records
        ]


        # =================================================
        # PREDICTION HISTORY
        # =================================================

        prediction_records = (
            PredictionHistory.query
            .order_by(
                PredictionHistory.created_at.asc()
            )
            .all()
        )


        prediction_records = prediction_records[-20:]


        prediction_dates = [
            record.created_at.strftime(
                "%d/%m %H:%M"
            )
            for record in prediction_records
        ]


        confidence = [
            record.confidence
            for record in prediction_records
        ]


        predictions = [
            record.prediction
            for record in prediction_records
        ]


        # =================================================
        # LATEST HEALTH DATA
        # =================================================

        latest_health = None

        if health_records:

            latest_health = health_records[-1]


        # =================================================
        # LATEST PREDICTION
        # =================================================

        latest_prediction = None

        if prediction_records:

            latest_prediction = prediction_records[-1]


        # =================================================
        # LATEST AI DATA
        # =================================================

        ai = {

            "prediction":
                0,

            "risk":
                "No Data",

            "confidence":
                0,

            "stroke_probability":
                0,

            "normal_probability":
                0

        }


        if latest_prediction:

            prediction_text = (
                latest_prediction.prediction
                or "No Data"
            )


            if "High" in prediction_text:

                prediction_value = 1
                risk = "High Risk"

            else:

                prediction_value = 0
                risk = "Low Risk"


            ai = {

                "prediction":
                    prediction_value,

                "risk":
                    risk,

                "confidence":
                    latest_prediction.confidence
                    or 0,

                "stroke_probability":
                    0,

                "normal_probability":
                    latest_prediction.confidence
                    or 0

            }


        # =================================================
        # LATEST HEALTH
        # =================================================

        health = {

            "heart_rate":
                latest_health.heart_rate
                if latest_health else 0,

            "spo2":
                latest_health.spo2
                if latest_health else 0,

            "steps":
                latest_health.steps
                if latest_health else 0,

            "calories":
                latest_health.calories
                if latest_health else 0,

            "distance":
                latest_health.distance
                if latest_health else 0,

            "sleep":
                latest_health.sleep
                if latest_health else 0

        }


        # =================================================
        # RESPONSE
        # =================================================

        return jsonify({

            "status":
                "success",

            # Health chart
            "dates":
                dates,

            "heartRate":
                heart_rate,

            "spo2":
                spo2,

            "steps":
                steps,

            "calories":
                calories,

            # AI chart
            "predictionDates":
                prediction_dates,

            "confidence":
                confidence,

            "predictions":
                predictions,

            # Latest data
            "health":
                health,

            "ai":
                ai

        })


    except Exception as e:

        print(
            "Dashboard Data Error:",
            e
        )

        return jsonify({

            "status":
                "error",

            "message":
                str(e)

        }), 500