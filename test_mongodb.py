import os

from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

uri = os.getenv("MONGO_URI")

client = MongoClient(
    uri,
    serverSelectionTimeoutMS=5000,
)

try:
    client.admin.command("ping")
    print("MongoDB connection successful")

except Exception as e:
    print("MongoDB connection failed:")
    print(repr(e))

finally:
    client.close()