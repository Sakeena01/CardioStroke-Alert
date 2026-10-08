from app import app
from models.health_data import HealthData
from models.user import User


with app.app_context():

    print("=" * 70)
    print("SPO2 DATA QUALITY CHECK")
    print("=" * 70)

    user = User.query.first()

    if not user:
        print("ERROR: No user found.")
        raise SystemExit

    records = (
        HealthData.query
        .filter(HealthData.user_id == user.id)
        .order_by(HealthData.created_at.asc())
        .all()
    )

    print("User ID:", user.id)
    print("Total records:", len(records))
    print()

    print("-" * 70)
    print(
        f"{'ID':<5}"
        f"{'Date/Time':<22}"
        f"{'HR':<8}"
        f"{'SpO2':<8}"
        f"{'Steps':<10}"
        f"{'Source':<18}"
    )
    print("-" * 70)

    for record in records:

        created = (
            record.created_at.strftime("%d/%m/%Y %H:%M:%S")
            if record.created_at
            else "--"
        )

        spo2 = record.spo2
        heart_rate = record.heart_rate
        steps = record.steps

        print(
            f"{record.id:<5}"
            f"{created:<22}"
            f"{str(heart_rate):<8}"
            f"{str(spo2):<8}"
            f"{str(steps):<10}"
            f"{str(record.source):<18}"
        )

    print("-" * 70)

    print()
    print("=" * 70)
    print("SUSPICIOUS SpO2 VALUES")
    print("=" * 70)

    suspicious = []

    for record in records:

        if record.spo2 is not None:

            if record.spo2 < 85 or record.spo2 > 100:
                suspicious.append(record)

    if suspicious:

        print(
            f"Found {len(suspicious)} suspicious SpO2 records."
        )

        print()

        for record in suspicious:

            print(
                "ID:",
                record.id,
                "| SpO2:",
                record.spo2,
                "| Date:",
                record.created_at
            )

    else:

        print(
            "No obviously invalid SpO2 values (<85 or >100) found."
        )

    print()
    print("=" * 70)
    print("CHECK COMPLETED")
    print("=" * 70)
    print("No database records were modified.")