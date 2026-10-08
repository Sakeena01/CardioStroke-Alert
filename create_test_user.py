from app import app
from models.user import db, User


with app.app_context():

    # Check if a user already exists
    user = User.query.first()

    if user:
        print("User already exists.")
        print("User ID:", user.id)
        print("Name:", user.name)

    else:

        user = User(
            fullname="Test User",
            email="sakeena.9739@gmail.com",
            password="test123",

            # Health profile
            age=45,
            bmi=24.5,
            glucose=95,
            systolic_bp=120,
            diastolic_bp=80
        )

        db.session.add(user)
        db.session.commit()

        print("Test user created successfully!")
        print("User ID:", user.id)