from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    fullname = db.Column(
        db.String(100),
        nullable=False
    )

    age = db.Column(
        db.Integer,
        nullable=True
    )

    gender = db.Column(
        db.String(20),
        nullable=True
    )

    email = db.Column(
        db.String(120),
        unique=True,
        nullable=False
    )

    password = db.Column(
        db.String(255),
        nullable=False
    )

    # ==========================================
    # HEALTH PROFILE
    # ==========================================

    bmi = db.Column(
        db.Float,
        nullable=True
    )

    glucose = db.Column(
        db.Float,
        nullable=True
    )

    systolic_bp = db.Column(
        db.Float,
        nullable=True
    )

    diastolic_bp = db.Column(
        db.Float,
        nullable=True
    )