import sqlite3

db_path = "instance/users.db"

connection = sqlite3.connect(db_path)

cursor = connection.cursor()

# Check existing columns
columns = [
    row[1]
    for row in cursor.execute(
        "PRAGMA table_info(health_data)"
    ).fetchall()
]

# Add source column if it doesn't exist
if "source" not in columns:
    cursor.execute(
        """
        ALTER TABLE health_data
        ADD COLUMN source VARCHAR(100)
        DEFAULT 'Health Connect'
        """
    )
    print("Added: source")
else:
    print("source already exists")

# Add device_name column if it doesn't exist
if "device_name" not in columns:
    cursor.execute(
        """
        ALTER TABLE health_data
        ADD COLUMN device_name VARCHAR(100)
        DEFAULT 'Unknown'
        """
    )
    print("Added: device_name")
else:
    print("device_name already exists")

connection.commit()
connection.close()

print("Database update completed successfully.")