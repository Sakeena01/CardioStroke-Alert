import sqlite3

db_path = "instance/users.db"

connection = sqlite3.connect(db_path)

print("TABLES:")
print(
    connection.execute(
        "SELECT name FROM sqlite_master WHERE type='table'"
    ).fetchall()
)

print("\nHEALTH DATA SCHEMA:")

print(
    connection.execute(
        "PRAGMA table_info(health_data)"
    ).fetchall()
)

connection.close()
