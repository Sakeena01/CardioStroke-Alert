import sqlite3
import os


DB_PATH = os.path.join(
    os.path.dirname(__file__),
    "instance",
    "users.db"
)


new_columns = {
    "age": "INTEGER",
    "bmi": "REAL",
    "glucose": "REAL",
    "systolic_bp": "REAL",
    "diastolic_bp": "REAL"
}


connection = sqlite3.connect(DB_PATH)
cursor = connection.cursor()


# Get existing columns
cursor.execute("PRAGMA table_info(user)")
existing_columns = {
    row[1]
    for row in cursor.fetchall()
}


for column, data_type in new_columns.items():

    if column not in existing_columns:

        cursor.execute(
            f"ALTER TABLE user ADD COLUMN {column} {data_type}"
        )

        print(f"Added column: {column}")

    else:

        print(f"Already exists: {column}")


connection.commit()
connection.close()


print("\nDatabase migration completed successfully.")