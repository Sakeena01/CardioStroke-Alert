import numpy as np

from ml.predictor import predict_health


def create_automatic_prediction(user, health_data):
    """
    Automatically predicts stroke risk from the latest wearable /
    Health Connect data.

    Wearable model uses exactly 8 features:

        1. age
        2. heart_rate
        3. spo2
        4. systolic BP
        5. diastolic BP
        6. BMI
        7. glucose
        8. steps

    ECG and fall are NOT required.

    Glucose handling:

    - Values greater than 30 are treated as mg/dL.
    - Values 30 or below are treated as mmol/L and converted
      to mg/dL using:

          mg/dL = mmol/L × 18.018

    This prevents values such as 95 mg/dL from incorrectly
    becoming 1711.71 mg/dL.
    """

    try:

        # ============================================================
        # 1. GET USER PROFILE VALUES
        # ============================================================

        age = getattr(
            user,
            "age",
            None
        )

        bmi = getattr(
            user,
            "bmi",
            None
        )


        # ============================================================
        # 2. GET HEALTH CONNECT VALUES
        # ============================================================

        heart_rate = getattr(
            health_data,
            "heart_rate",
            None
        )

        spo2 = getattr(
            health_data,
            "spo2",
            None
        )

        steps = getattr(
            health_data,
            "steps",
            None
        )


        # ============================================================
        # 3. BLOOD PRESSURE
        # ============================================================

        systolic_bp = getattr(
            health_data,
            "systolic_bp",
            None
        )

        diastolic_bp = getattr(
            health_data,
            "diastolic_bp",
            None
        )


        if systolic_bp is None:

            systolic_bp = getattr(
                user,
                "systolic_bp",
                None
            )


        if diastolic_bp is None:

            diastolic_bp = getattr(
                user,
                "diastolic_bp",
                None
            )


        # ============================================================
        # 4. BLOOD GLUCOSE
        # ============================================================

        glucose = getattr(
            health_data,
            "blood_glucose",
            None
        )


        if glucose is None:

            glucose = getattr(
                user,
                "glucose",
                None
            )


        # ============================================================
        # 5. CHECK REQUIRED VALUES
        # ============================================================

        missing = []


        if age is None:
            missing.append("age")

        if heart_rate is None:
            missing.append("heart_rate")

        if spo2 is None:
            missing.append("spo2")

        if systolic_bp is None:
            missing.append("sbp")

        if diastolic_bp is None:
            missing.append("dbp")

        if bmi is None:
            missing.append("bmi")

        if glucose is None:
            missing.append("glucose")

        if steps is None:
            missing.append("steps")


        # ============================================================
        # STOP IF REQUIRED DATA IS MISSING
        # ============================================================

        if missing:

            print()
            print("==============================================")
            print(" AUTOMATIC PREDICTION - MISSING DATA")
            print("==============================================")

            print(
                "Missing:",
                ", ".join(missing)
            )

            print("==============================================")
            print()

            return {

                "success": False,

                "prediction": None,

                "risk": "Insufficient Data",

                "confidence": 0.0,

                "stroke_probability": 0.0,

                "normal_probability": 0.0,

                "message":
                    "Required health data is missing.",

                "missing":
                    missing
            }


        # ============================================================
        # 6. CONVERT VALUES TO NUMERIC
        # ============================================================

        age = float(age)

        heart_rate = float(
            heart_rate
        )

        spo2 = float(
            spo2
        )

        systolic_bp = float(
            systolic_bp
        )

        diastolic_bp = float(
            diastolic_bp
        )

        bmi = float(
            bmi
        )

        glucose = float(
            glucose
        )

        steps = float(
            steps
        )


        # ============================================================
        # 7. NORMALIZE GLUCOSE
        #
        # If the incoming value is already in mg/dL,
        # keep it unchanged.
        #
        # If it is a small mmol/L value, convert it.
        # ============================================================

        original_glucose = glucose

        if glucose <= 30:

            glucose = glucose * 18.018

            glucose_unit = "mmol/L -> mg/dL"

        else:

            glucose_unit = "mg/dL"


        # ============================================================
        # 8. CREATE EXACT 8-FEATURE MODEL INPUT
        # ============================================================

        model_input = np.array(
            [
                age,
                heart_rate,
                spo2,
                systolic_bp,
                diastolic_bp,
                bmi,
                glucose,
                steps
            ],
            dtype=float
        )


        # ============================================================
        # 9. XGBOOST PREDICTION
        # ============================================================

        (
            prediction,
            confidence,
            stroke_probability,
            normal_probability
        ) = predict_health(
            model_input
        )


        # ============================================================
        # 10. STANDARD PYTHON TYPES
        # ============================================================

        prediction = int(
            prediction
        )

        confidence = float(
            confidence
        )

        stroke_probability = float(
            stroke_probability
        )

        normal_probability = float(
            normal_probability
        )


        # ============================================================
        # 11. RISK LABEL
        # ============================================================

        if prediction == 1:

            risk = "High Risk"

        else:

            risk = "Low Risk"


        # ============================================================
        # 12. TERMINAL OUTPUT
        # ============================================================

        print()
        print("==============================================")
        print("       AUTOMATIC HEALTH PREDICTION")
        print("==============================================")

        print(
            "User ID:",
            user.id
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
            "Systolic BP:",
            systolic_bp
        )

        print(
            "Diastolic BP:",
            diastolic_bp
        )

        print(
            "BMI:",
            bmi
        )

        print(
            "Original Glucose:",
            original_glucose
        )

        print(
            "Glucose Unit Handling:",
            glucose_unit
        )

        print(
            "Model Glucose:",
            glucose,
            "mg/dL"
        )

        print(
            "Steps:",
            steps
        )

        print("----------------------------------------------")

        print(
            "Prediction:",
            prediction
        )

        print(
            "Risk:",
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

        print("==============================================")
        print()


        # ============================================================
        # 13. RETURN COMPLETE AUTOMATIC RESULT
        # ============================================================

        return {

            "success":
                True,

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

            "age":
                age,

            "heart_rate":
                heart_rate,

            "spo2":
                spo2,

            "systolic_bp":
                systolic_bp,

            "diastolic_bp":
                diastolic_bp,

            "bmi":
                bmi,

            "glucose":
                glucose,

            "steps":
                steps,

            "message":
                "Automatic health prediction completed successfully."
        }


    # ================================================================
    # ERROR HANDLING
    # ================================================================

    except Exception as e:

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
        print()

        import traceback

        traceback.print_exc()


        return {

            "success":
                False,

            "prediction":
                None,

            "risk":
                "Unknown Risk",

            "confidence":
                0.0,

            "stroke_probability":
                0.0,

            "normal_probability":
                0.0,

            "message":
                "Automatic prediction failed.",

            "error":
                str(e)
        }