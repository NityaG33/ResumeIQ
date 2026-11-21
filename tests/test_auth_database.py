
import uuid
import pytest

from database.connection import (
    client,
    DATABASE_NAME,
    users_collection
)

from auth.service import (
    create_user,
    get_user_by_email,
    get_user_by_id
)

from auth.password import verify_password


@pytest.fixture
def test_email():
    email = f"test_{uuid.uuid4().hex}@example.com"

    yield email

    # Clean up the test user after execution
    users_collection.delete_one({"email": email})


# 1. Test actual user creation in MongoDB
def test_create_user_in_database(test_email):
    result = create_user(
        test_email,
        "password123"
    )

    assert result["id"] is not None
    assert result["email"] == test_email

    # Verify that the user actually exists in MongoDB
    user = users_collection.find_one({
        "email": test_email
    })

    assert user is not None
    assert user["email"] == test_email


# 2. Test password hashing during user creation
def test_user_password_is_hashed(test_email):
    create_user(
        test_email,
        "password123"
    )

    user = get_user_by_email(test_email)

    assert user is not None
    assert user["password_hash"] != "password123"

    assert verify_password(
        "password123",
        user["password_hash"]
    )

    assert not verify_password(
        "wrongpassword",
        user["password_hash"]
    )


# 3. Test retrieving user by email
def test_get_user_by_email(test_email):
    create_user(
        test_email,
        "password123"
    )

    user = get_user_by_email(test_email)

    assert user is not None
    assert user["email"] == test_email


# 4. Test retrieving user by ID
def test_get_user_by_id(test_email):
    created_user = create_user(
        test_email,
        "password123"
    )

    user = get_user_by_id(created_user["id"])

    assert user is not None
    assert str(user["_id"]) == created_user["id"]
    assert user["email"] == test_email


# 5. Test invalid user ID
def test_get_user_by_invalid_id():
    user = get_user_by_id("invalid_object_id")

    assert user is None


# 6. Verify MongoDB test database connection
def test_mongodb_test_database_connection():
    assert DATABASE_NAME == "resumeiq_test"

    result = client.admin.command("ping")

    assert result["ok"] == 1



