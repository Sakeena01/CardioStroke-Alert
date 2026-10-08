from app import app
from models.user import db
from sqlalchemy import inspect


with app.app_context():

    inspector = inspect(db.engine)

    # Check whether health_data table exists
    tables = inspector.get_table_names()

    if "health_data" not in tables:
        print("ERROR: health_data table does not exist.")
        raise SystemExit

    columns = {
        column["name"]
        for column in inspector.get_columns("health_data")
    }

    print("Existing health_data columns:")
    for column in sorted(columns):
        print(" -", column)

    # Columns required by the current HealthData model
    required_columns = {
        "systolic_bp": "FLOAT",
        "diastolic_bp": "FLOAT",
        "blood_glucose": "FLOAT",
    }

    with db.engine.begin() as connection:

        for column_name, column_type in required_columns.items():

            if column_name not in columns:

                sql = (
                    f"ALTER TABLE health_data "
                    f"ADD COLUMN {column_name} {column_type}"
                )

                connection.exec_driver_sql(sql)

                print(
                    f"ADDED: {column_name} ({column_type})"
                )

            else:
                print(
                    f"OK: {column_name} already exists"
                )

    print()
    print("===================================")
    print("DATABASE MIGRATION COMPLETED")
    print("===================================")