from datetime import datetime, timezone

from pymongo.errors import DuplicateKeyError

from auth.password import hash_password
from database.connection import users_collection
from bson import ObjectId


def create_user(email: str, password: str) -> dict:

    email = email.lower().strip()

    user = {
        "email": email,
        "password_hash": hash_password(password),
        "created_at": datetime.now(timezone.utc),
    }

    try:
        result = users_collection.insert_one(user)

    except DuplicateKeyError:
        raise ValueError("Email already registered")

    return {
        "id": str(result.inserted_id),
        "email": email,
    }


def get_user_by_id(user_id: str) -> dict | None:

    try:
        object_id = ObjectId(user_id)
    except Exception:
        return None

    return users_collection.find_one({
        "_id": object_id
    })


def get_user_by_email(email: str) -> dict | None:

    email = email.lower().strip()

    return users_collection.find_one({
        "email": email
    })