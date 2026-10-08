import os
import requests

from dotenv import load_dotenv


# ============================================================
# LOAD ENVIRONMENT VARIABLES
# ============================================================

load_dotenv()


BREVO_API_KEY = os.getenv(
    "BREVO_API_KEY"
)

BREVO_SENDER_EMAIL = os.getenv(
    "BREVO_SENDER_EMAIL"
)

BREVO_SENDER_NAME = os.getenv(
    "BREVO_SENDER_NAME",
    "CardioStroke Alert"
)


# ============================================================
# BREVO API
# ============================================================

BREVO_URL = (
    "https://api.brevo.com/v3/smtp/email"
)


# ============================================================
# COMMON BREVO EMAIL FUNCTION
# ============================================================

def send_brevo_email(
    recipient,
    subject,
    body
):

    if not BREVO_API_KEY:

        print(
            "BREVO ERROR: BREVO_API_KEY is missing."
        )

        return False


    if not BREVO_SENDER_EMAIL:

        print(
            "BREVO ERROR: BREVO_SENDER_EMAIL is missing."
        )

        return False


    if not recipient:

        print(
            "BREVO ERROR: Recipient email is missing."
        )

        return False


    headers = {

        "accept":
            "application/json",

        "api-key":
            BREVO_API_KEY,

        "content-type":
            "application/json"

    }


    payload = {

        "sender": {

            "name":
                BREVO_SENDER_NAME,

            "email":
                BREVO_SENDER_EMAIL

        },

        "to": [

            {

                "email":
                    recipient

            }

        ],

        "subject":
            subject,

        "textContent":
            body

    }


    try:

        response = requests.post(

            BREVO_URL,

            headers=headers,

            json=payload,

            timeout=30

        )


        if response.status_code in (
            200,
            201,
            202
        ):

            print()
            print(
                "=============================================="
            )

            print(
                "BREVO EMAIL SENT SUCCESSFULLY"
            )

            print(
                "Recipient:",
                recipient
            )

            print(
                "Sender:",
                BREVO_SENDER_EMAIL
            )

            print(
                "Subject:",
                subject
            )

            try:

                response_data = (
                    response.json()
                )

                print(
                    "Message ID:",
                    response_data.get(
                        "messageId"
                    )
                )

            except Exception:

                pass


            print(
                "=============================================="
            )

            return True


        print()
        print(
            "=============================================="
        )

        print(
            "BREVO EMAIL ERROR"
        )

        print(
            "Status:",
            response.status_code
        )

        print(
            "Response:",
            response.text
        )

        print(
            "=============================================="
        )

        return False


    except Exception as e:

        print()
        print(
            "=============================================="
        )

        print(
            "BREVO CONNECTION ERROR"
        )

        print(
            type(e).__name__
        )

        print(
            str(e)
        )

        print(
            "=============================================="
        )

        return False


# ============================================================
# GENERIC / BACKWARD-COMPATIBLE FUNCTION
# ============================================================

def send_alert(
    app,
    recipient,
    result,
    subject=None,
    body=None
):

    if subject is None:

        subject = (
            "CardioStroke Alert - "
            "Health Risk Notification"
        )


    if body is None:

        body = (

            "CARDIOSTROKE ALERT\n\n"

            "Health Risk Notification\n\n"

            f"Prediction Result: {result}\n\n"

            "This notification was generated "
            "by the CardioStroke Alert system.\n\n"

            "Please consult a qualified "
            "medical professional for "
            "appropriate evaluation.\n\n"

            "CardioStroke Alert\n"
            "Automated Health Monitoring System"

        )


    return send_brevo_email(

        recipient=recipient,

        subject=subject,

        body=body

    )


# ============================================================
# MANUAL PREDICTION EMAIL
# ============================================================

def send_manual_prediction_email(

    recipient,

    prediction_result,

    risk_level,

    confidence,

    stroke_probability,

    normal_probability,

    health_score,

    age,

    heart_rate,

    spo2,

    sbp,

    dbp,

    bmi,

    glucose,

    steps,

    prediction_date,

    prediction_time

):

    subject = (
        "CardioStroke Alert - Manual Prediction - "
        f"{risk_level}"
    )

    body = (

        "CARDIOSTROKE ALERT\n"
        "MANUAL HEALTH PREDICTION\n"
        "====================================\n\n"

        f"Date: {prediction_date}\n"
        f"Prediction Time: {prediction_time}\n\n"

        "RISK LEVEL\n"
        "------------------------------------\n"

        f"Risk Level: {risk_level}\n\n"

        "MODEL PREDICTION\n"
        "------------------------------------\n"

        f"Prediction Result: {prediction_result}\n"

        f"Stroke Probability: "
        f"{float(stroke_probability):.2f}%\n"

        f"Confidence: "
        f"{float(confidence):.2f}%\n"

        f"Normal Probability: "
        f"{float(normal_probability):.2f}%\n\n"

        "HEALTH PARAMETERS\n"
        "------------------------------------\n"

        f"Age: {age}\n"

        f"Heart Rate: "
        f"{heart_rate} BPM\n"

        f"SpO2: "
        f"{spo2}%\n"

        f"Systolic BP: "
        f"{sbp} mmHg\n"

        f"Diastolic BP: "
        f"{dbp} mmHg\n"

        f"BMI: "
        f"{bmi}\n"

        f"Glucose: "
        f"{glucose} mg/dL\n"

        f"Steps: "
        f"{steps}\n\n"

        f"Health Score: "
        f"{health_score}\n\n"

        "MONITORING TYPE\n"
        "------------------------------------\n"

        "This is today's MANUAL prediction.\n"

        "The result is based on the health "
        "parameters entered during the manual "
        "prediction process.\n\n"

        "IMPORTANT\n"
        "------------------------------------\n"

        "This result is a prototype risk "
        "assessment and is not a medical "
        "diagnosis.\n\n"

        "Please consult a qualified medical "
        "professional for appropriate "
        "evaluation.\n\n"

        "CardioStroke Alert\n"
        "Automated Health Monitoring System"

    )

    return send_brevo_email(

        recipient=recipient,

        subject=subject,

        body=body

    )

# ============================================================
# 10-DAY MONITORING EMAIL
# ============================================================

def send_10_day_monitoring_email(

    recipient,

    observation_start,

    observation_end,

    days_observed,

    overall_risk,

    risk_score,

    trend,

    average_heart_rate,

    average_spo2,

    average_sbp,

    average_dbp,

    average_bmi,

    average_glucose,

    average_steps,

    risk_factors=None

):

    if risk_factors is None:

        risk_factors = []


    subject = (
        "CardioStroke Alert - "
        "10-Day Health Risk Report"
    )


    risk_factor_text = (

        "\n".join(

            [

                f"- {factor}"

                for factor in risk_factors

            ]

        )

        if risk_factors

        else

        "No significant risk factors recorded."

    )


    body = (

        "CARDIOSTROKE ALERT\n"

        "10-DAY HEALTH MONITORING REPORT\n"

        "====================================\n\n"


        "Observation Period\n"

        "------------------------------------\n"

        f"Start Date: {observation_start}\n"

        f"End Date: {observation_end}\n"

        f"Days Observed: {days_observed}/10\n\n"


        "Overall Monitoring Result\n"

        "------------------------------------\n"

        f"Overall Risk: {overall_risk}\n"

        f"Risk Score: {risk_score}\n"

        f"Health Trend: {trend}\n\n"


        "10-Day Health Summary\n"

        "------------------------------------\n"

        f"Average Heart Rate: "
        f"{average_heart_rate} BPM\n"

        f"Average SpO2: "
        f"{average_spo2}%\n"

        f"Average Systolic BP: "
        f"{average_sbp} mmHg\n"

        f"Average Diastolic BP: "
        f"{average_dbp} mmHg\n"

        f"Average BMI: "
        f"{average_bmi}\n"

        f"Average Glucose: "
        f"{average_glucose} mg/dL\n"

        f"Average Steps: "
        f"{average_steps}\n\n"


        "Risk Factors\n"

        "------------------------------------\n"

        f"{risk_factor_text}\n\n"


        "Monitoring Result\n"

        "------------------------------------\n"

        "This report is generated from "

        "health-monitoring data collected "

        "during the 10-day observation period.\n\n"


        "The 10-day monitoring report is "

        "independent of today's manual "

        "prediction email.\n\n"


        "Important\n"

        "------------------------------------\n"

        "This report represents a prototype "

        "risk assessment and is not a medical "

        "diagnosis.\n\n"

        "Please consult a qualified medical "

        "professional for appropriate "

        "evaluation.\n\n"


        "CardioStroke Alert\n"

        "10-Day Monitoring System"

    )


    return send_brevo_email(

        recipient=recipient,

        subject=subject,

        body=body

    )