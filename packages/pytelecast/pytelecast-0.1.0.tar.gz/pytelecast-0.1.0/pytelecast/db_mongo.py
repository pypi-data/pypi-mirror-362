# pytelecast/db_mongo.py

from pymongo import MongoClient

def setup_mongo(db_url: str):
    client = MongoClient(db_url)
    db = client["broadcast_bot"]
    users_col = db["users"]

    def add_user(user_id: int):
        users_col.update_one({"user_id": user_id}, {"$set": {"user_id": user_id}}, upsert=True)

    def get_all_users() -> list[int]:
        return [doc["user_id"] for doc in users_col.find({}, {"_id": 0, "user_id": 1})]

    return add_user, get_all_users