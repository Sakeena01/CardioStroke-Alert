import sqlite3
import os

db_path = os.path.abspath("instance/users.db")

print("DATABASE:")
print(db_path)

connection = sqlite3.connect(db_path)
cursor = connection.cursor()

print("\nUSER TABLE:")
print(
    cursor.execute(
        "PRAGMA table_info(user)"
    ).fetchall()
)

print("\nUSER COUNT:")
print(
    cursor.execute(
        "SELECT COUNT(*) FROM user"
    ).fetchone()
)

connection.close()