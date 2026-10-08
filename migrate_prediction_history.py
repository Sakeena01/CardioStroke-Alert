import sqlite3
import os

DB_PATH = os.path.join("instance", "users.db")

print("======================================")
print("Prediction History Database Migration")
print("======================================")

if not os.path.exists(DB_PATH):
    print("ERROR: Database not found:")
    print(DB_PATH)
    raise SystemExit

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Get existing columns
cursor.execute("PRAGMA table_info(prediction_history)")
existing_columns = {
    row[1]
    for row in cursor.fetchall()
}

print("\nExisting columns:")
print(existing_columns)

# Columns required by the current PredictionHistory model
columns_to_add = {
    "user_id": "INTEGER",
    "systolic_bp": "FLOAT",
    "diastolic_bp": "FLOAT",
    "stroke_probability": "FLOAT",
    "normal_probability": "FLOAT",
}

for column, column_type in columns_to_add.items():

    if column not in existing_columns:

        sql = f"""
        ALTER TABLE prediction_history
        ADD COLUMN {column} {column_type}
        """

        cursor.execute(sql)

        print(f"Added column: {column}")

    else:

        print(f"Already exists: {column}")

conn.commit()

# Verify final schema
print("\n======================================")
print("FINAL prediction_history SCHEMA")
print("======================================")

cursor.execute("PRAGMA table_info(prediction_history)")

for row in cursor.fetchall():
    print(row)

conn.close()

print("\nMigration completed successfully.")