def clean_number(value):
    if value is None:
        return None

    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def clean_spo2(value):
    value = clean_number(value)

    if value is None:
        return None

    if 70 <= value <= 100:
        return value

    print(f"WARNING: Invalid SpO2 received: {value}")
    print("SpO2 will be stored as NULL.")

    return None


def clean_heart_rate(value):
    value = clean_number(value)

    if value is None:
        return None

    if value > 0:
        return value

    print(f"WARNING: Invalid heart rate received: {value}")

    return None


def clean_steps(value):
    value = clean_number(value)

    if value is None:
        return None

    if value >= 0:
        return value

    print(f"WARNING: Invalid steps received: {value}")

    return None


def clean_optional(value):
    return clean_number(value)