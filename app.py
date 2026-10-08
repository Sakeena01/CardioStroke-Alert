from flask import Flask, redirect, url_for
from flask_mail import Mail
from api.dashboard_api import dashboard_api_bp
from models.user import db
from api.auto_prediction import auto_prediction_bp
from routes.prediction import prediction_bp
from routes.dashboard import dashboard_bp
from routes.analytics import analytics_bp
from routes.report import report_bp
from routes.health3d import health3d_bp
from routes.api import api_bp
from routes.history import history_bp
from api.health_api import health_api
from models.health_alert import HealthAlert
from routes.alert_history import alert_history_bp
# ============================================================
# CREATE FLASK APP
# ============================================================

app = Flask(__name__)

app.config["SECRET_KEY"] = "major_project_secret_key"


# ============================================================
# DATABASE CONFIGURATION
# ============================================================

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)


# ============================================================
# EMAIL CONFIGURATION
# ============================================================

mail = Mail()

app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True

app.config["MAIL_USERNAME"] = "YOUR_EMAIL@gmail.com"
app.config["MAIL_PASSWORD"] = "YOUR_APP_PASSWORD"

mail.init_app(app)


# ============================================================
# REGISTER BLUEPRINTS
# ============================================================
app.register_blueprint(auto_prediction_bp)
app.register_blueprint(prediction_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(analytics_bp)
app.register_blueprint(report_bp)
app.register_blueprint(health3d_bp)
app.register_blueprint(api_bp)
app.register_blueprint(history_bp)
# Health Connect / Android API
app.register_blueprint(health_api)
app.register_blueprint(dashboard_api_bp)
app.register_blueprint(alert_history_bp)
# ============================================================
# HOME
# ============================================================

@app.route("/")
def home():
    return redirect(url_for("dashboard.dashboard"))


# ============================================================
# CREATE DATABASE TABLES
# ============================================================

with app.app_context():
    db.create_all()


# ============================================================
# RUN APPLICATION
# ============================================================

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )