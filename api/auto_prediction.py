from flask import Blueprint, request, jsonify

from models.user import User, db
from models.health_data import HealthData
from models.prediction_history import PredictionHistory

from ml.automatic_prediction import create_automatic_prediction
from ml.explainable_ai import explain_prediction


# =========================================================
# BLUEPRINT
# =========================================================

automatic_prediction_bp = Blueprint(
    "automatic_prediction",
    __name__,
    url_prefix="/api"
)


# =========================================================
# AUTOMATIC PREDICTION
# =========================================================

@automatic_prediction_bp.route(
    "/automatic_prediction",
    methods=["POST"]
)
def automatic_prediction():

    try:

        # =================================================
        # GET REQUEST DATA
        # =================================================

        data = request.get_json() or {}

        user_id = data.get("user_id")

        if not user_id:
            return jsonify({
                "status": "error",
                "message": "user_id is required"
            }), 400


        # =================================================
        # FIND USER
        # =================================================

        user = User.query.get(user_id)

        if user is None:
            return jsonify({
                "status": "error",
                "message": "User not found"
            }), 404


        # =================================================
        # GET LATEST HEALTH DATA
        # =================================================

        health_data = (
            HealthData.query
            .filter_by(user_id=user_id)
            .order_by(
                HealthData.created_at.desc()
            )
            .first()
        )

        if health_data is None:
            return jsonify({
                "status": "error",
                "message": "No health data available for this user"
            }), 404


        # =================================================
        # CREATE AUTOMATIC XGBOOST PREDICTION
        # =================================================

        result = create_automatic_prediction(
            user,
            health_data
        )


        # =================================================
        # CHECK PREDICTION RESULT
        # =================================================

        if not result.get("success"):

            return jsonify({
                "status": "incomplete",
                "message": result.get(
                    "message",
                    "Required health data is missing."
                ),
                "missing": result.get(
                    "missing",
                    []
                )
            }), 400


        # =================================================
        # GET MODEL OUTPUT
        # =================================================

        prediction_value = int(
            result.get(
                "prediction",
                0
            )
        )

        confidence = float(
            result.get(
                "confidence",
                0
            )
        )

        stroke_probability = float(
            result.get(
                "stroke_probability",
                0
            )
        )

        normal_probability = float(
            result.get(
                "normal_probability",
                0
            )
        )


        # =================================================
        # DETERMINE RISK
        # =================================================

        if prediction_value == 1:
            risk = "High Risk"
        else:
            risk = "Low Risk"


        # =================================================
        # GET MODEL FEATURES
        #
        # 8 FEATURES:
        #
        # age
        # heart_rate
        # spo2
        # sbp
        # dbp
        # bmi
        # glucose
        # steps
        # =================================================

        age = user.age

        heart_rate = health_data.heart_rate

        spo2 = health_data.spo2

        sbp = user.systolic_bp

        dbp = user.diastolic_bp

        bmi = user.bmi

        glucose = user.glucose

        steps = health_data.steps


        # =================================================
        # EXPLAINABLE AI
        # =================================================

        explanation_data = explain_prediction(

            age=age,

            heart_rate=heart_rate,

            spo2=spo2,

            sbp=sbp,

            dbp=dbp,

            bmi=bmi,

            glucose=glucose,

            steps=steps,

            prediction=prediction_value,

            confidence=confidence

        )


        # =================================================
        # SAVE PREDICTION HISTORY
        #
        # IMPORTANT:
        # PredictionHistory uses:
        # systolic_bp
        # diastolic_bp
        #
        # NOT sbp / dbp.
        # =================================================

        history = PredictionHistory(

            user_id=user.id,

            age=age,

            heart_rate=heart_rate,

            spo2=spo2,

            systolic_bp=sbp,

            diastolic_bp=dbp,

            glucose=glucose,

            bmi=bmi,

            steps=steps,

            prediction=risk,

            confidence=confidence,

            stroke_probability=stroke_probability,

            normal_probability=normal_probability

        )


        # =================================================
        # SAVE DATABASE
        # =================================================

        db.session.add(history)

        db.session.commit()


        # =================================================
        # TERMINAL OUTPUT
        # =================================================

        print()
        print("==============================================")
        print("       AUTOMATIC HEALTH PREDICTION")
        print("==============================================")

        print(
            "History ID:",
            history.id
        )

        print(
            "User ID:",
            user.id
        )

        print(
            "Prediction:",
            risk
        )

        print(
            "Confidence:",
            confidence
        )

        print(
            "Stroke Probability:",
            stroke_probability
        )

        print(
            "Normal Probability:",
            normal_probability
        )

        print("----------------------------------------------")
        print("             XAI ANALYSIS")
        print("----------------------------------------------")

        print(
            "High Factors:",
            explanation_data.get(
                "high_count",
                0
            )
        )

        print(
            "Moderate Factors:",
            explanation_data.get(
                "moderate_count",
                0
            )
        )

        print(
            "Normal Factors:",
            explanation_data.get(
                "normal_count",
                0
            )
        )

        print("----------------------------------------------")

        for factor in explanation_data.get(
            "factors",
            []
        ):

            print(
                factor.get("name"),
                ":",
                factor.get("value"),
                "->",
                factor.get("severity")
            )

        print("==============================================")
        print()


        # =================================================
        # API RESPONSE
        # =================================================

        return jsonify({

            "status": "success",

            "source":
                health_data.source
                if health_data.source
                else "Health Connect",

            "device_name":
                health_data.device_name
                if health_data.device_name
                else "Unknown",

            "prediction":
                prediction_value,

            "risk":
                risk,

            "confidence":
                confidence,

            "stroke_probability":
                stroke_probability,

            "normal_probability":
                normal_probability,

            "history_id":
                history.id,


            # =================================================
            # FEATURES
            # =================================================

            "features": {

                "age":
                    age,

                "heart_rate":
                    heart_rate,

                "spo2":
                    spo2,

                "sbp":
                    sbp,

                "dbp":
                    dbp,

                "bmi":
                    bmi,

                "glucose":
                    glucose,

                "steps":
                    steps

            },


            # =================================================
            # XAI
            # =================================================

            "explanation": {

                "summary":
                    explanation_data.get(
                        "summary",
                        ""
                    ),

                "high_count":
                    explanation_data.get(
                        "high_count",
                        0
                    ),

                "moderate_count":
                    explanation_data.get(
                        "moderate_count",
                        0
                    ),

                "normal_count":
                    explanation_data.get(
                        "normal_count",
                        0
                    ),

                "high_factors":
                    explanation_data.get(
                        "high_factors",
                        []
                    ),

                "moderate_factors":
                    explanation_data.get(
                        "moderate_factors",
                        []
                    ),

                "normal_factors":
                    explanation_data.get(
                        "normal_factors",
                        []
                    ),

                "factors":
                    explanation_data.get(
                        "factors",
                        []
                    )

            }

        }), 200


    # =====================================================
    # ERROR HANDLING
    # =====================================================

    except Exception as e:

        db.session.rollback()

        print()
        print("==============================================")
        print("      AUTOMATIC PREDICTION ERROR")
        print("==============================================")
        print(
            type(e).__name__
        )
        print(
            str(e)
        )
        print("==============================================")

        import traceback

        traceback.print_exc()

        return jsonify({

            "status": "error",

            "message":
                "Unable to generate automatic prediction.",

            "error":
                str(e)

        }), 500


# =========================================================
# EXPORT BLUEPRINT
# =========================================================

auto_prediction_bp = automatic_prediction_bp