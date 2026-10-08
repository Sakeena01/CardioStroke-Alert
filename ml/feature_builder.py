def build_ml_features(
    user,
    health_data,
    ecg=None,
    fall=None
):
    """
    Build the feature vector required by the existing
    stroke prediction model.

    Feature order:
    1. age
    2. heart_rate
    3. spo2
    4. systolic_bp
    5. diastolic_bp
    6. bmi
    7. glucose
    8. steps
    9. ecg
    10. fall
    """

    # ---------------------------------------------
    # Validate required profile information
    # ---------------------------------------------

    missing = []

    if user.age is None:
        missing.append("age")

    if user.bmi is None:
        missing.append("bmi")

    if user.glucose is None:
        missing.append("glucose")

    if user.systolic_bp is None:
        missing.append("systolic_bp")

    if user.diastolic_bp is None:
        missing.append("diastolic_bp")

    # ---------------------------------------------
    # Validate required wearable information
    # ---------------------------------------------

    if health_data.heart_rate is None:
        missing.append("heart_rate")

    if health_data.spo2 is None:
        missing.append("spo2")

    if health_data.steps is None:
        missing.append("steps")

    # ---------------------------------------------
    # ECG and fall
    # ---------------------------------------------

    # These are not currently provided by the
    # Health Connect payload.
    #
    # We therefore DO NOT invent medical values.
    #
    # For the current automatic pipeline, they must
    # be explicitly supplied by another supported
    # source or by the testing system.

    if ecg is None:
        missing.append("ecg")

    if fall is None:
        missing.append("fall")

    # ---------------------------------------------
    # Stop if required features are missing
    # ---------------------------------------------

    if missing:

        return {
            "success": False,
            "missing": missing,
            "features": None
        }

    # ---------------------------------------------
    # Create feature vector
    # ---------------------------------------------

    features = [
        user.age,
        health_data.heart_rate,
        health_data.spo2,
        user.systolic_bp,
        user.diastolic_bp,
        user.bmi,
        user.glucose,
        health_data.steps,
        ecg,
        fall
    ]

    return {
        "success": True,
        "missing": [],
        "features": features
    }