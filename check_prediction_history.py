import sqlite3

connection = sqlite3.connect("instance/users.db")
cursor = connection.cursor()

print("PREDICTION HISTORY TABLE:")

print(
    cursor.execute(
        "PRAGMA table_info(prediction_history)"
    ).fetchall()
)

print("\nPREDICTION RECORDS:")

records = cursor.execute(
    """
    SELECT
        id,
        age,
        heart_rate,
        spo2,
        glucose,
        bmi,
        steps,
        prediction,
        confidence,
        created_at
    FROM prediction_history
    ORDER BY id DESC
    """
).fetchall()

for record in records:
    print(record)

connection.close()