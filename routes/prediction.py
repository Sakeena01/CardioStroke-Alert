from flask import (
    Blueprint,
    render_template,
    request,
    current_app
)

import numpy as np
import os
from datetime import datetime
from zoneinfo import ZoneInfo

from models.user import db
from models.prediction_history import PredictionHistory

from ml.predictor import predict_health
from ml.health_score import calculate_health_score
from ml.risk_forecast import forecast
from ml.recommendation import recommendation

# IMPORTANT:
# Use only this XAI module.
from ml.explainable_ai import explain_prediction

# IMPORTANT:
# Email alert function
from routes.email_alert import send_manual_prediction_email


# =========================================================
# BLUEPRINT
# =========================================================

prediction_bp = Blueprint(
    "prediction",
    __name__
)


# =========================================================
# PREDICTION PAGE
# =========================================================

@prediction_bp.route(
    "/prediction",
    methods=["GET"]
)
def prediction():

    return render_template(
        "prediction.html"
    )


# =========================================================
# MANUAL PREDICTION
# =========================================================

@prediction_bp.route(
    "/predict",
    methods=["POST"]
)
def predict():

    try:

        # =================================================
        # GET FORM DATA
        # =================================================

        age = float(
            request.form.get(
                "age",
                0
            )
        )

        heart_rate = float(
            request.form.get(
                "heart_rate",
                0
            )
        )

        spo2 = float(
            request.form.get(
                "spo2",
                0
            )
        )

        sbp = float(
            request.form.get(
                "sbp",
                0
            )
        )

        dbp = float(
            request.form.get(
                "dbp",
                0
            )
        )

        bmi = float(
            request.form.get(
                "bmi",
                0
            )
        )

        glucose = float(
            request.form.get(
                "glucose",
                0
            )
        )

        steps = float(
            request.form.get(
                "steps",
                0
            )
        )

        # =================================================
        # GET EMAIL
        # =================================================

        email = request.form.get(
            "email"
        )

        if email:
            email = email.strip()

        # =================================================
        # BASIC VALIDATION
        # =================================================

        values = {

            "age": age,

            "heart_rate": heart_rate,

            "spo2": spo2,

            "sbp": sbp,

            "dbp": dbp,

            "bmi": bmi,

            "glucose": glucose,

            "steps": steps

        }

        for name, value in values.items():

            if not np.isfinite(value):

                return render_template(
                    "prediction.html",
                    error=(
                        f"Invalid value for {name}."
                    )
                )


        # =================================================
        # CREATE MODEL INPUT
        #
        # WEARABLE MODEL = 8 FEATURES
        #
        # 1. age
        # 2. heart_rate
        # 3. spo2
        # 4. sbp
        # 5. dbp
        # 6. bmi
        # 7. glucose
        # 8. steps
        #
        # ECG and FALL are NOT used here.
        # =================================================

        data = np.array([

            age,

            heart_rate,

            spo2,

            sbp,

            dbp,

            bmi,

            glucose,

            steps

        ])


        # =================================================
        # ML PREDICTION
        # =================================================

        (
            prediction_value,
            confidence,
            stroke_probability,
            normal_probability

        ) = predict_health(
            data
        )


        # =================================================
        # HEALTH SCORE
        # =================================================

        health_score = calculate_health_score(

            heart_rate,

            spo2,

            bmi,

            glucose,

            steps

        )


        # =================================================
        # RISK FORECAST
        # =================================================

        risk = forecast(
            health_score
        )


        # =================================================
        # RECOMMENDATIONS
        # =================================================

        tips = recommendation(
            health_score
        )


        # =================================================
        # DETERMINE PREDICTION RESULT
        # =================================================

        if int(prediction_value) == 1:

            result = "⚠ High Risk"

            explanation = (
                "The current health parameters indicate "
                "an elevated stroke risk. Immediate medical "
                "consultation is recommended."
            )

        else:

            result = "✅ Low Risk"

            explanation = (
                "Current health parameters indicate "
                "a low stroke risk."
            )


        # =================================================
        # EXPLAINABLE AI
        #
        # IMPORTANT:
        # This MUST be inside the predict() function
        # because all these variables come from the form.
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

            prediction=int(
                prediction_value
            ),

            confidence=confidence

        )


        # =================================================
        # SAVE PREDICTION HISTORY
        # =================================================

        history = PredictionHistory(

            age=age,

            heart_rate=heart_rate,

            spo2=spo2,

            glucose=glucose,

            bmi=bmi,

            systolic_bp=sbp,

            diastolic_bp=dbp,

            steps=steps,

            prediction=result,

            confidence=confidence,

            stroke_probability=stroke_probability,

            normal_probability=normal_probability

        )


        # =================================================
        # SAVE TO DATABASE
        # =================================================

        db.session.add(
            history
        )

        db.session.commit()


        # =================================================
        # IMMEDIATE MANUAL EMAIL ALERT
        #
        # Send the manual prediction email for all three
        # supported risk levels:
        # Low Risk, Moderate Risk and High Risk.
        #
        # The fixed recipient from .env is preferred.
        # The email entered in the form is used only as a
        # fallback when ALERT_RECIPIENT is not configured.
        # =================================================

        email_sent = False

        try:

            # -------------------------------------------------
            # NORMALIZE RISK LEVEL
            # -------------------------------------------------

            risk_text = str(
                risk
            ).strip()

            risk_lower = risk_text.lower()

            if "high risk" in risk_lower:

                manual_risk = "High Risk"

            elif (
                "moderate risk" in risk_lower
                or "medium risk" in risk_lower
            ):

                manual_risk = "Moderate Risk"

            else:

                manual_risk = "Low Risk"

            # -------------------------------------------------
            # GET RECIPIENT
            # -------------------------------------------------

            recipient = (
                os.getenv(
                    "ALERT_RECIPIENT"
                )
                or email
            )

            print()
            print(
                "======================================"
            )
            print(
                "      MANUAL EMAIL ALERT"
            )
            print(
                "======================================"
            )

            print(
                "Recipient:",
                recipient if recipient else "Not configured"
            )

            print(
                "Risk Level:",
                manual_risk
            )

            print(
                "Prediction:",
                result
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
                "--------------------------------------"
            )

            # -------------------------------------------------
            # SEND EMAIL WHEN A RECIPIENT IS AVAILABLE
            # -------------------------------------------------

            if recipient:

                india_now = datetime.now(
                    ZoneInfo("Asia/Kolkata")
                )

                prediction_date = india_now.strftime(
                    "%d %B %Y"
                )

                prediction_time = india_now.strftime(
                    "%I:%M %p"
                )

                email_sent = send_manual_prediction_email(

                    recipient=recipient,

                    prediction_result=result,

                    risk_level=manual_risk,

                    confidence=confidence,

                    stroke_probability=stroke_probability,

                    normal_probability=normal_probability,

                    health_score=health_score,

                    age=age,

                    heart_rate=heart_rate,

                    spo2=spo2,

                    sbp=sbp,

                    dbp=dbp,

                    bmi=bmi,

                    glucose=glucose,

                    steps=steps,

                    prediction_date=prediction_date,

                    prediction_time=prediction_time

                )

                if email_sent:

                    print(
                        "BREVO EMAIL SENT SUCCESSFULLY"
                    )

                    print(
                        "Recipient:",
                        recipient
                    )

                    print(
                        "Risk Level:",
                        manual_risk
                    )

                else:

                    print(
                        "BREVO EMAIL FAILED"
                    )

            else:

                print(
                    "No email recipient configured."
                )

        except Exception as email_error:

            print(
                "Manual Email Alert Error:",
                email_error
            )

        # =================================================
        # TERMINAL LOG
        # =================================================

        print(
            "======================================"
        )

        print(
            "Prediction saved successfully"
        )

        print(
            "History ID:",
            history.id
        )

        print(
            "Age:",
            age
        )

        print(
            "Heart Rate:",
            heart_rate
        )

        print(
            "SpO2:",
            spo2
        )

        print(
            "SBP:",
            sbp
        )

        print(
            "DBP:",
            dbp
        )

        print(
            "BMI:",
            bmi
        )

        print(
            "Glucose:",
            glucose
        )

        print(
            "Steps:",
            steps
        )

        print(
            "Prediction:",
            result
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

        print(
            "Health Score:",
            health_score
        )

        print(
            "Email:",
            email if email else "Not provided"
        )

        print(
            "Email Sent:",
            email_sent
        )

        print(
            "XAI High Factors:",
            explanation_data[
                "high_count"
            ]
        )

        print(
            "XAI Moderate Factors:",
            explanation_data[
                "moderate_count"
            ]
        )

        print(
            "XAI Normal Factors:",
            explanation_data[
                "normal_count"
            ]
        )

        print(
            "======================================"
        )


        # =================================================
        # RETURN RESULT
        # =================================================

        return render_template(

            "prediction.html",

            prediction=prediction_value,

            result=result,

            confidence=confidence,

            stroke_probability=stroke_probability,

            normal_probability=normal_probability,

            health_score=health_score,

            risk=risk,

            tips=tips,

            explanation=explanation,

            explanation_data=explanation_data,

            age=age,

            heart_rate=heart_rate,

            spo2=spo2,

            sbp=sbp,

            dbp=dbp,

            bmi=bmi,

            glucose=glucose,

            steps=steps,

            email=email,

            email_sent=email_sent

        )


    # =====================================================
    # ERROR HANDLING
    # =====================================================

    except Exception as e:

        db.session.rollback()

        print(
            "======================================"
        )

        print(
            "Prediction Error:"
        )

        print(
            type(e).__name__
        )

        print(
            str(e)
        )

        import traceback

        traceback.print_exc()

        print(
            "======================================"
        )

        return render_template(

            "prediction.html",

            error=(
                "Unable to generate prediction. "
                "Please check the entered values."
            )

        )


# =========================================================
# END OF FILE
# =========================================================