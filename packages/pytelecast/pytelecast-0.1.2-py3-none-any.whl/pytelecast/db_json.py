# pytelecast/db_json.py

import json
import os

DB_FILE = "users.json"

def add_user(user_id: int):
    users = []
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f:
            try:
                users = json.load(f)
            except json.JSONDecodeError:
                users = []

    if user_id not in users:
        users.append(user_id)
        with open(DB_FILE, "w") as f:
            json.dump(users, f)

def get_all_users() -> list[int]:
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []
