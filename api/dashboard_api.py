from flask import Blueprint, jsonify

from models.health_data import HealthData
from models.user import User

from ml.health_score import calculate_health_score
from ml.automatic_prediction import create_automatic_prediction


dashboard_api_bp = Blueprint(
    "dashboard_api",
    __name__,
    url_prefix="/api"
)


@dashboard_api_bp.route(
    "/dashboard_data",
    methods=["GET"]
)
def dashboard_data():

    try:

        # =================================================
        # GET USER
        # =================================================

        user = User.query.first()

        if user is None:

            return jsonify({
                "status": "error",
                "message": "No user found"
            }), 404


        # =================================================
        # GET LATEST HEALTH CONNECT DATA
        # =================================================

        latest = (
            HealthData.query
            .order_by(
                HealthData.created_at.desc()
            )
            .first()
        )

        if latest is None:

            return jsonify({
                "status": "error",
                "message": "No health data available"
            }), 404


        # =================================================
        # HEALTH SCORE
        # =================================================

        health_score = calculate_health_score(

            latest.heart_rate or 0,

            latest.spo2 or 0,

            user.bmi or 0,

            user.glucose or 0,

            latest.steps or 0
        )


        # =================================================
        # AUTOMATIC AI PREDICTION
        # =================================================

        result = create_automatic_prediction(
            user,
            latest
        )


        # =================================================
        # DEFAULT AI VALUES
        # =================================================

        prediction = None

        risk = "Incomplete Data"

        confidence = 0

        stroke_probability = 0

        normal_probability = 0

        missing = []


        # =================================================
        # PREDICTION RESULT
        # =================================================

        if result["success"]:

            prediction = result["prediction"]

            confidence = result["confidence"]

            stroke_probability = (
                result["stroke_probability"]
            )

            normal_probability = (
                result["normal_probability"]
            )


            if prediction == 1:

                risk = "High Risk"

            else:

                risk = "Low Risk"

        else:

            missing = result.get(
                "missing",
                []
            )


        # =================================================
        # RESPONSE
        # =================================================

        return jsonify({

            "status": "success",

            "timestamp": (
                latest.created_at.isoformat()
                if latest.created_at
                else None
            ),

            "device_name": (
                latest.device_name
                if latest.device_name
                else "Unknown"
            ),

            "source": (
                latest.source
                if latest.source
                else "Health Connect"
            ),

            "health": {

                "heart_rate":
                    latest.heart_rate or 0,

                "spo2":
                    latest.spo2 or 0,

                "steps":
                    latest.steps or 0,

                "calories":
                    latest.calories or 0,

                "distance":
                    latest.distance or 0,

                "sleep":
                    latest.sleep or 0
            },

            "profile": {

                "age":
                    user.age or 0,

                "bmi":
                    user.bmi or 0,

                "glucose":
                    user.glucose or 0,

                "systolic_bp":
                    user.systolic_bp or 0,

                "diastolic_bp":
                    user.diastolic_bp or 0
            },

            "ai": {

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

                "missing":
                    missing
            },

            "health_score":
                health_score

        }), 200


    except Exception as e:

        print(
            "Dashboard API Error:",
            e
        )

        return jsonify({

            "status": "error",

            "message":
                "Unable to load dashboard data.",

            "error":
                str(e)

        }), 500