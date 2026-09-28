import os

from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
DATABASE_NAME = os.getenv("DATABASE_NAME", "resumeiq")

if not MONGO_URI:
    raise RuntimeError("MONGO_URI is not configured")

client = MongoClient(
    MONGO_URI,
    serverSelectionTimeoutMS=5000,
)

db = client[DATABASE_NAME]

users_collection = db["users"]
resumes_collection = db["resumes"]
analyses_collection = db["analyses"]

users_collection.create_index(
    "email",
    unique=True
)