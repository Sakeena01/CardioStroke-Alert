import os

from dotenv import load_dotenv

from models.user import db
from models.health_alert import HealthAlert
from ml.thirty_day_risk import analyze_10_day_risk
from routes.email_alert import send_10_day_monitoring_email


# ==========================================================
# LOAD ENVIRONMENT VARIABLES
# ==========================================================

load_dotenv()

ALERT_RECIPIENT = os.getenv(
    "ALERT_RECIPIENT"
)


# ==========================================================
# 10-DAY HEALTH ALERT PROCESSOR
# ==========================================================

def process_10_day_alert(app, user):

    try:

        # --------------------------------------------------
        # RUN 10-DAY ANALYSIS
        # --------------------------------------------------

        analysis = analyze_10_day_risk(
            user.id
        )

        if not analysis.get("success"):

            return {
                "success": False,
                "alert_sent": False,
                "message": "10-day analysis failed.",
                "analysis": analysis
            }

        # --------------------------------------------------
        # GET ANALYSIS RESULT
        # --------------------------------------------------

        days_observed = analysis.get(
            "days_observed",
            0
        )

        risk = analysis.get(
            "risk",
            "Low Risk"
        )

        risk_score = analysis.get(
            "risk_score",
            0
        )

        trend = analysis.get(
            "trend",
            "Stable"
        )

        factors = analysis.get(
            "risk_factors",
            []
        )

        # --------------------------------------------------
        # GET OBSERVATION PERIOD
        # --------------------------------------------------

        observation_start = analysis.get(
            "observation_start",
            ""
        )

        observation_end = analysis.get(
            "observation_end",
            ""
        )

        averages = analysis.get(
            "averages",
            {}
        )

        average_heart_rate = averages.get(
            "heart_rate",
            0
        )

        average_spo2 = averages.get(
            "spo2",
            0
        )

        average_sbp = averages.get(
            "sbp",
            0
        )

        average_dbp = averages.get(
            "dbp",
            0
        )

        average_bmi = averages.get(
            "bmi",
            0
        )

        average_glucose = averages.get(
            "glucose",
            0
        )

        average_steps = averages.get(
            "steps",
            0
        )

        # --------------------------------------------------
        # WAIT UNTIL ALL 10 DAYS ARE OBSERVED
        # --------------------------------------------------

        if days_observed < 10:

            return {
                "success": True,
                "alert_sent": False,
                "message":
                    f"Only {days_observed}/10 days observed. "
                    "Waiting for sufficient data.",
                "analysis": analysis
            }

        # --------------------------------------------------
        # NORMALIZE RISK LABEL
        # --------------------------------------------------

        risk = str(
            risk
        ).strip()

        allowed_risks = {
            "Low Risk",
            "Moderate Risk",
            "High Risk"
        }

        # --------------------------------------------------
        # ONLY LOW / MODERATE / HIGH
        # --------------------------------------------------

        if risk not in allowed_risks:

            return {
                "success": True,
                "alert_sent": False,
                "message":
                    f"No email sent because risk is "
                    f"'{risk}'.",
                "analysis": analysis
            }

        # --------------------------------------------------
        # CREATE RISK-SPECIFIC ALERT TYPE
        # --------------------------------------------------

        alert_type = (
            "10_DAY_"
            + risk.upper().replace(
                " ",
                "_"
            )
        )

        # --------------------------------------------------
        # CHECK DUPLICATE ALERT
        # --------------------------------------------------
        #
        # This prevents the same risk-level email from
        # being sent repeatedly.
        #
        # Example:
        # Low -> Low -> Low
        # only sends the first Low Risk email.
        #
        # If later it becomes:
        # Moderate Risk
        # a new email is sent.
        #
        # If later it becomes:
        # High Risk
        # another new email is sent.
        # --------------------------------------------------

        previous_alert = (
            HealthAlert.query
            .filter_by(
                user_id=user.id,
                alert_type=alert_type
            )
            .first()
        )

        if previous_alert:

            return {
                "success": True,
                "alert_sent": False,
                "message":
                    f"{risk} alert already sent previously.",
                "analysis": analysis
            }

        # --------------------------------------------------
        # GET RECIPIENT
        # --------------------------------------------------
        #
        # ALERT_RECIPIENT from .env is preferred.
        # user.email is used only as fallback.
        # --------------------------------------------------

        recipient = (
            ALERT_RECIPIENT
            or getattr(
                user,
                "email",
                None
            )
        )

        if not recipient:

            return {
                "success": False,
                "alert_sent": False,
                "message":
                    "Recipient email address is not available.",
                "analysis": analysis
            }

        # --------------------------------------------------
        # SEND 10-DAY EMAIL
        # --------------------------------------------------

        email_sent = (
            send_10_day_monitoring_email(

                recipient=recipient,

                observation_start=(
                    observation_start
                ),

                observation_end=(
                    observation_end
                ),

                days_observed=(
                    days_observed
                ),

                overall_risk=(
                    risk
                ),

                risk_score=(
                    risk_score
                ),

                trend=(
                    trend
                ),

                average_heart_rate=(
                    average_heart_rate
                ),

                average_spo2=(
                    average_spo2
                ),

                average_sbp=(
                    average_sbp
                ),

                average_dbp=(
                    average_dbp
                ),

                average_bmi=(
                    average_bmi
                ),

                average_glucose=(
                    average_glucose
                ),

                average_steps=(
                    average_steps
                ),

                risk_factors=(
                    factors
                )
            )
        )

        # --------------------------------------------------
        # EMAIL FAILED
        # --------------------------------------------------

        if not email_sent:

            return {
                "success": False,
                "alert_sent": False,
                "message":
                    f"{risk} result detected, "
                    "but email could not be sent.",
                "analysis": analysis
            }

        # --------------------------------------------------
        # SAVE ALERT
        # --------------------------------------------------

        alert = HealthAlert(

            user_id=user.id,

            alert_type=(
                alert_type
            ),

            risk=(
                risk
            ),

            risk_score=(
                risk_score
            )

        )

        db.session.add(
            alert
        )

        db.session.commit()

        # --------------------------------------------------
        # SUCCESS LOG
        # --------------------------------------------------

        print()
        print(
            "=============================================="
        )
        print(
            "       10-DAY HEALTH ALERT SENT"
        )
        print(
            "=============================================="
        )

        print(
            "User ID:",
            user.id
        )

        print(
            "Recipient:",
            recipient
        )

        print(
            "Risk:",
            risk
        )

        print(
            "Risk Score:",
            risk_score
        )

        print(
            "Trend:",
            trend
        )

        print(
            "Days Observed:",
            days_observed
        )

        print(
            "Alert Type:",
            alert_type
        )

        print(
            "HealthAlert ID:",
            alert.id
        )

        print(
            "=============================================="
        )

        # --------------------------------------------------
        # RETURN SUCCESS
        # --------------------------------------------------

        return {
            "success": True,
            "alert_sent": True,
            "message":
                f"{risk} 10-day health monitoring "
                "email sent successfully.",
            "analysis": analysis
        }

    except Exception as error:

        db.session.rollback()

        print()
        print(
            "=============================================="
        )

        print(
            "       10-DAY ALERT ERROR"
        )

        print(
            "=============================================="
        )

        print(
            type(error).__name__
        )

        print(
            error
        )

        print(
            "=============================================="
        )

        return {
            "success": False,
            "alert_sent": False,
            "message":
                "10-day alert processing failed.",
            "error": str(
                error
            ),
            "analysis": {}
        }