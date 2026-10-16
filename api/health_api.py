from flask import Blueprint, request, jsonify, current_app

from models.user import db, User
from models.health_data import HealthData
from models.prediction_history import PredictionHistory

from ml.automatic_prediction import create_automatic_prediction
from ml.thirty_day_alert import process_10_day_alert

from utils.health_validation import (
    clean_spo2,
    clean_heart_rate,
    clean_steps,
    clean_optional
)


health_api = Blueprint("health_api", __name__)


@health_api.route("/sync_health", methods=["POST"])
def sync_health():

    try:

        # ==========================================================
        # 1. GET JSON DATA
        # ==========================================================

        data = request.get_json()

        if not data:
            return jsonify({
                "status": "error",
                "message": "No JSON data received"
            }), 400


        # ==========================================================
        # 2. GET USER
        # ==========================================================
        user_id = data.get("user_id")

        # DEBUG: Check the ID received from Android
        print("\n========== USER ID DEBUG ==========")
        print("Received user_id:", repr(user_id))
        print(
            "Users in this database:",
            [(u.id, u.fullname) for u in User.query.all()]
        )
        print("===================================\n")

        if user_id is None or str(user_id).strip() == "":
            return jsonify({
                "status": "error",
                "message": "user_id is required"
            }), 400

        try:
            user_id = int(user_id)
        except (TypeError, ValueError):
            return jsonify({
                "status": "error",
                "message": "user_id must be a valid integer"
            }), 400

        user = db.session.get(User, user_id)

        if user is None:
            print("DEBUG: User ID does not exist:", user_id)

            return jsonify({
                "status": "error",
                "message": "User not found",
                "received_user_id": user_id
            }), 404

        print("DEBUG: Matched user:", user.id, user.fullname)


        # ==========================================================
        # 3. HEALTH CONNECT DATA
        # ==========================================================

        heart_rate = clean_heart_rate(
            data.get("heart_rate")
        )

        spo2 = clean_spo2(
            data.get("spo2")
        )

        steps = clean_steps(
            data.get("steps")
        )

        calories = clean_optional(
            data.get("calories")
        )

        distance = clean_optional(
            data.get("distance")
        )

        sleep = clean_optional(
            data.get("sleep")
        )


        # ==========================================================
        # 4. BLOOD PRESSURE
        # ==========================================================

        sbp = data.get("sbp")

        if sbp is None:
            sbp = data.get("systolic_bp")

        if sbp is None:
            sbp = data.get("systolicBP")

        sbp = clean_optional(sbp)


        dbp = data.get("dbp")

        if dbp is None:
            dbp = data.get("diastolic_bp")

        if dbp is None:
            dbp = data.get("diastolicBP")

        dbp = clean_optional(dbp)


        # ==========================================================
        # 5. BLOOD GLUCOSE
        # ==========================================================

        glucose = data.get("glucose")

        if glucose is None:
            glucose = data.get("blood_glucose")

        if glucose is None:
            glucose = data.get("bloodGlucose")

        glucose = clean_optional(glucose)


        # ==========================================================
        # 6. SOURCE / DEVICE
        # ==========================================================

        source = data.get(
            "source",
            "Health Connect"
        )

        device_name = data.get(
            "device_name",
            "Unknown"
        )


        # ==========================================================
        # 7. TERMINAL LOG
        # ==========================================================

        print()
        print("==============================================")
        print("          AUTOMATIC HEALTH SYNC")
        print("==============================================")

        print("User ID:", user.id)
        print("Device:", device_name)
        print("Source:", source)

        print("----------------------------------------------")

        print("Heart Rate:", heart_rate)
        print("SpO2:", spo2)
        print("Steps:", steps)
        print("Calories:", calories)
        print("Distance:", distance)
        print("Sleep:", sleep)
        print("SBP:", sbp)
        print("DBP:", dbp)
        print("Glucose:", glucose)

        print("==============================================")


        # ==========================================================
        # 8. SAVE HEALTH DATA
        # ==========================================================

        health_record = HealthData(
            user_id=user.id,
            heart_rate=heart_rate,
            spo2=spo2,
            steps=steps,
            calories=calories,
            distance=distance,
            sleep=sleep,
            systolic_bp=sbp,
            diastolic_bp=dbp,
            blood_glucose=glucose,
            source=source,
            device_name=device_name
        )

        db.session.add(health_record)

        db.session.commit()


        print()
        print("Health data saved successfully.")

        print(
            "HealthData ID:",
            health_record.id
        )


        # ==========================================================
        # 9. AUTOMATIC XGBOOST PREDICTION
        # ==========================================================

        automatic_result = None

        history_id = None


        try:

            automatic_result = create_automatic_prediction(
                user,
                health_record
            )


        except Exception as prediction_error:

            print()
            print("==============================================")
            print("      AUTOMATIC PREDICTION ERROR")
            print("==============================================")

            print(
                type(prediction_error).__name__
            )

            print(
                str(prediction_error)
            )

            print("==============================================")


            automatic_result = {

                "success": False,

                "prediction": None,

                "risk": "Unknown Risk",

                "confidence": 0.0,

                "stroke_probability": 0.0,

                "normal_probability": 0.0,

                "message":
                    "Automatic prediction failed.",

                "error":
                    str(prediction_error)
            }


        # ==========================================================
        # 10. DISPLAY AUTOMATIC PREDICTION
        # ==========================================================

        print()
        print("==============================================")
        print("       AUTOMATIC XGBOOST RESULT")
        print("==============================================")


        print(
            "Success:",
            automatic_result.get(
                "success",
                False
            )
        )

        print(
            "Prediction:",
            automatic_result.get(
                "prediction"
            )
        )

        print(
            "Risk:",
            automatic_result.get(
                "risk"
            )
        )

        print(
            "Confidence:",
            automatic_result.get(
                "confidence",
                0
            )
        )

        print(
            "Stroke Probability:",
            automatic_result.get(
                "stroke_probability",
                0
            )
        )

        print(
            "Normal Probability:",
            automatic_result.get(
                "normal_probability",
                0
            )
        )

        print(
            "Missing:",
            automatic_result.get(
                "missing",
                []
            )
        )

        print("==============================================")


        # ==========================================================
        # 11. SAVE AUTOMATIC PREDICTION TO HISTORY
        # ==========================================================

        if automatic_result.get("success"):

            prediction_value = automatic_result.get(
                "prediction"
            )


            if prediction_value is not None:

                prediction_value = int(
                    prediction_value
                )


                if prediction_value == 1:

                    prediction_label = "High Risk"

                else:

                    prediction_label = "Low Risk"


                history = PredictionHistory(

                    user_id=user.id,

                    age=automatic_result.get(
                        "age"
                    ),

                    heart_rate=automatic_result.get(
                        "heart_rate"
                    ),

                    spo2=automatic_result.get(
                        "spo2"
                    ),

                    glucose=automatic_result.get(
                        "glucose"
                    ),

                    bmi=automatic_result.get(
                        "bmi"
                    ),

                    systolic_bp=automatic_result.get(
                        "systolic_bp"
                    ),

                    diastolic_bp=automatic_result.get(
                        "diastolic_bp"
                    ),

                    steps=automatic_result.get(
                        "steps"
                    ),

                    prediction=prediction_label,

                    confidence=automatic_result.get(
                        "confidence",
                        0
                    ),

                    stroke_probability=automatic_result.get(
                        "stroke_probability",
                        0
                    ),

                    normal_probability=automatic_result.get(
                        "normal_probability",
                        0
                    )
                )


                db.session.add(history)

                db.session.commit()


                history_id = history.id


                print()
                print("==============================================")
                print("   AUTOMATIC PREDICTION SAVED TO HISTORY")
                print("==============================================")

                print(
                    "History ID:",
                    history.id
                )

                print(
                    "Prediction:",
                    history.prediction
                )

                print(
                    "Confidence:",
                    history.confidence
                )

                print(
                    "Stroke Probability:",
                    history.stroke_probability
                )

                print(
                    "Normal Probability:",
                    history.normal_probability
                )

                print("==============================================")


        else:

            print()
            print(
                "Prediction was NOT saved to history."
            )

            print(
                "Reason:",
                automatic_result.get(
                    "message",
                    "Insufficient data"
                )
            )


        # ==========================================================
        # 12. 30-DAY ALERT PROCESSING
        # ==========================================================

        try:

            alert_result = process_10_day_alert(

                app=current_app._get_current_object(),

                user=user
            )


        except Exception as alert_error:

            print()
            print(
                "10-Day Alert Error:",
                alert_error
            )


            alert_result = {

                "success": False,

                "alert_sent": False,

                "message":
                    "Health data saved, but 10-day alert analysis failed.",

                "error":
                    str(alert_error),

                "analysis": {}
            }


        # ==========================================================
        # 13. GET 30-DAY ANALYSIS
        # ==========================================================

        analysis = alert_result.get(
            "analysis",
            {}
        )


        # ==========================================================
        # 14. FINAL API RESPONSE
        # ==========================================================

        response = {

            "status": "success",

            "message":
                "Health data saved and processed successfully.",


            # ======================================================
            # SAVED HEALTH DATA
            # ======================================================

            "data": {

                "id":
                    health_record.id,

                "user_id":
                    health_record.user_id,

                "heart_rate":
                    health_record.heart_rate,

                "spo2":
                    health_record.spo2,

                "steps":
                    health_record.steps,

                "calories":
                    health_record.calories,

                "distance":
                    health_record.distance,

                "sleep":
                    health_record.sleep,

                "systolic_bp":
                    health_record.systolic_bp,

                "diastolic_bp":
                    health_record.diastolic_bp,

                "blood_glucose":
                    health_record.blood_glucose,

                "source":
                    health_record.source,

                "device_name":
                    health_record.device_name
            },


            # ======================================================
            # AUTOMATIC XGBOOST PREDICTION
            # ======================================================

            "automatic_prediction": {

                "success":
                    automatic_result.get(
                        "success",
                        False
                    ),

                "prediction":
                    automatic_result.get(
                        "prediction"
                    ),

                "risk":
                    automatic_result.get(
                        "risk"
                    ),

                "confidence":
                    automatic_result.get(
                        "confidence",
                        0
                    ),

                "stroke_probability":
                    automatic_result.get(
                        "stroke_probability",
                        0
                    ),

                "normal_probability":
                    automatic_result.get(
                        "normal_probability",
                        0
                    ),

                "history_id":
                    history_id,

                "missing_data":
                    automatic_result.get(
                        "missing",
                        []
                    ),

                "message":
                    automatic_result.get(
                        "message"
                    )
            },


            # ======================================================
            # 30-DAY ANALYSIS
            # ======================================================

            "10_day_analysis": {

                "days_observed":
                    analysis.get(
                        "days_observed",
                        0
                    ),

                "total_records":
                    analysis.get(
                        "total_records",
                        0
                    ),

                "observation_status":
                    analysis.get(
                        "observation_status",
                        "Collecting data"
                    ),

                "risk":
                    analysis.get(
                        "risk",
                        "No Data"
                    ),

                "risk_score":
                    analysis.get(
                        "risk_score",
                        0
                    ),

                "overall_risk":
                    analysis.get(
                        "overall_risk",
                        "No Data"
                    ),

                "overall_risk_score":
                    analysis.get(
                        "overall_risk_score",
                        0
                    ),

                "recent_risk":
                    analysis.get(
                        "recent_risk",
                        "No Data"
                    ),

                "recent_risk_score":
                    analysis.get(
                        "recent_risk_score",
                        0
                    ),

                "previous_risk":
                    analysis.get(
                        "previous_risk",
                        "No Data"
                    ),

                "previous_risk_score":
                    analysis.get(
                        "previous_risk_score",
                        0
                    ),

                "trend":
                    analysis.get(
                        "trend",
                        "Insufficient Data"
                    ),

                "trend_score":
                    analysis.get(
                        "trend_score",
                        0
                    ),

                "direction":
                    analysis.get(
                        "direction",
                        "Collecting data"
                    ),

                "recent_records":
                    analysis.get(
                        "recent_records",
                        0
                    ),

                "previous_records":
                    analysis.get(
                        "previous_records",
                        0
                    ),

                "average_heart_rate":
                    analysis.get(
                        "average_heart_rate"
                    ),

                "average_spo2":
                    analysis.get(
                        "average_spo2"
                    ),

                "average_steps":
                    analysis.get(
                        "average_steps"
                    ),

                "average_sleep":
                    analysis.get(
                        "average_sleep"
                    ),

                "risk_factors":
                    analysis.get(
                        "risk_factors",
                        []
                    ),

                "alert_sent":
                    alert_result.get(
                        "alert_sent",
                        False
                    ),

                "alert_type":
                    alert_result.get(
                        "alert_type"
                    ),

                "alert_message":
                    alert_result.get(
                        "message"
                    )
            }
        }


        # ==========================================================
        # 15. RETURN RESPONSE
        # ==========================================================

        return jsonify(response), 200


    # ==============================================================
    # 16. GLOBAL ERROR HANDLING
    # ==============================================================

    except Exception as e:

        db.session.rollback()

        print()
        print("==============================================")
        print("             HEALTH SYNC ERROR")
        print("==============================================")

        print(
            "Error Type:",
            type(e).__name__
        )

        print(
            "Error:",
            str(e)
        )

        print("==============================================")


        return jsonify({

            "status":
                "error",

            "message":
                str(e)

        }), 500