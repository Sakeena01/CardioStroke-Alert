import os

from dotenv import load_dotenv

from routes.email_alert import send_alert


load_dotenv()


recipient = os.getenv(
    "ALERT_RECIPIENT"
)


print()
print("============================================================")
print("BREVO EMAIL TEST")
print("============================================================")

print(
    "Recipient:",
    recipient
)

print(
    "API Key configured:",
    bool(os.getenv("BREVO_API_KEY"))
)

print(
    "Sender:",
    os.getenv("BREVO_SENDER_EMAIL")
)

print("------------------------------------------------------------")


result = send_alert(

    recipient=recipient,

    result="TEST ALERT - Email system is working",

    subject="CardioStroke Alert - Test Email",

    body="""
CardioStroke Alert

This is a test email.

The Brevo email notification system is working correctly.

This email was generated from the Flask application.
"""
)


print("------------------------------------------------------------")

print(
    "Email result:",
    result
)

print("============================================================")