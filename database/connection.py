import os

from dotenv import load_dotenv
from pymongo import MongoClient


load_dotenv()


MONGO_URI = os.getenv("MONGO_URI")
DATABASE_NAME = os.getenv("DATABASE_NAME", "resumeiq")


if not MONGO_URI:
    raise RuntimeError("MONGO_URI is not configured")


client = MongoClient(MONGO_URI)

client.admin.command("ping")
print("Connected to MongoDB Atlas successfully!")

db = client[DATABASE_NAME]

users_collection = db["users"]

users_collection.create_index(
    "email",
    unique=True
)