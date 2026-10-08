import sqlite3

db_path = "instance/users.db"

connection = sqlite3.connect(db_path)
cursor = connection.cursor()

columns = [
    row[1]
    for row in cursor.execute(
        "PRAGMA table_info(health_data)"
    ).fetchall()
]

if "user_id" not in columns:
    cursor.execute(
        """
        ALTER TABLE health_data
        ADD COLUMN user_id INTEGER
        """
    )
    print("Added: user_id")
else:
    print("user_id already exists")

connection.commit()
connection.close()

print("Health database update completed.")