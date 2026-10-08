import sqlite3
import os

DB_PATH = "instance/database.db"

if not os.path.exists(DB_PATH):
    print("ERROR: Database file not found:")
    print(DB_PATH)
    raise SystemExit

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

cursor.execute("PRAGMA table_info(health_data)")
columns = [row[1] for row in cursor.fetchall()]

print("Existing health_data columns:")
print(columns)

columns_to_add = {
    "systolic_bp": "REAL",
    "diastolic_bp": "REAL",
    "blood_glucose": "REAL"
}

for column, data_type in columns_to_add.items():
    if column not in columns:
        print(f"Adding column: {column}")
        cursor.execute(
            f"ALTER TABLE health_data ADD COLUMN {column} {data_type}"
        )
    else:
        print(f"Already exists: {column}")

conn.commit()

cursor.execute("PRAGMA table_info(health_data)")
final_columns = [row[1] for row in cursor.fetchall()]

print("\nFinal health_data columns:")
print(final_columns)

conn.close()

print("\nDatabase fix completed successfully.")