# pytelecast/db_sqlite.py

import sqlite3

# Connect to database (creates file if not exist)
conn = sqlite3.connect("users.db", check_same_thread=False)
cursor = conn.cursor()

# Create table once
cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY
    )
""")
conn.commit()

# Function to add user
def add_user(user_id: int):
    try:
        cursor.execute("INSERT OR IGNORE INTO users (user_id) VALUES (?)", (user_id,))
        conn.commit()
        print(f"👤 User {user_id} added to SQLite DB.")
    except Exception as e:
        print(f"⚠️ Error adding user {user_id}: {e}")

# Function to get all users
def get_all_users() -> list[int]:
    cursor.execute("SELECT user_id FROM users")
    return [row[0] for row in cursor.fetchall()]