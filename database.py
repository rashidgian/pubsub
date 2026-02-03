from pymongo import MongoClient
import os

def get_db():
    mongo_host = os.environ.get("MONGO_HOST", "mongo")
    mongo_port = int(os.environ.get("MONGO_PORT", 27017))
    mongo_username = os.environ.get("MONGO_USERNAME", "main")
    mongo_password = os.environ.get("MONGO_PASSWORD", "main123")
    client = MongoClient(f"mongodb://{mongo_username}:{mongo_password}@{mongo_host}:{mongo_port}/", serverSelectionTimeoutMS=5000)
    db = client["my_articles_db"]
    return db["articles"]