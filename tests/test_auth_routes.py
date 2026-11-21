
import os

# Set a placeholder MongoDB URI before importing the app.
# We will mock database operations in these tests.
os.environ.setdefault("MONGO_URI", "mongodb://localhost:27017")

import pytest
from fastapi.testclient import TestClient

from api import app
from auth.dependencies import get_current_user


@pytest.fixture
def client():
    return TestClient(app)


# 1. Successful registration
def test_register_success(client, monkeypatch):
    def mock_create_user(email, password):
        return {
            "id": "123",
            "email": email.lower()
        }

    monkeypatch.setattr(
        "auth.routes.create_user",
        mock_create_user
    )

    response = client.post(
        "/api/v1/auth/register",
        json={
            "email": "test@example.com",
            "password": "password123"
        }
    )

    assert response.status_code == 201
    assert response.json()["email"] == "test@example.com"


# 2. Registration with an existing email
def test_register_duplicate_email(client, monkeypatch):
    def mock_create_user(email, password):
        raise ValueError("Email already registered")

    monkeypatch.setattr(
        "auth.routes.create_user",
        mock_create_user
    )

    response = client.post(
        "/api/v1/auth/register",
        json={
            "email": "test@example.com",
            "password": "password123"
        }
    )

    assert response.status_code == 409
    assert response.json()["detail"] == "Email already registered"


# 3. Successful login
def test_login_success(client, monkeypatch):
    monkeypatch.setattr(
        "auth.routes.get_user_by_email",
        lambda email: {
            "_id": "123",
            "email": email,
            "password_hash": "hashed_password"
        }
    )

    monkeypatch.setattr(
        "auth.routes.verify_password",
        lambda password, hashed: True
    )

    monkeypatch.setattr(
        "auth.routes.create_access_token",
        lambda data: "test-jwt-token"
    )

    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": "test@example.com",
            "password": "password123"
        }
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Login successful"
    assert response.cookies.get("access_token") == "test-jwt-token"


# 4. Login with invalid credentials
def test_login_invalid_password(client, monkeypatch):
    monkeypatch.setattr(
        "auth.routes.get_user_by_email",
        lambda email: {
            "_id": "123",
            "email": email,
            "password_hash": "hashed_password"
        }
    )

    monkeypatch.setattr(
        "auth.routes.verify_password",
        lambda password, hashed: False
    )

    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": "test@example.com",
            "password": "wrongpassword"
        }
    )

    assert response.status_code == 401


# 5. Accessing profile without authentication
def test_get_me_unauthenticated(client):
    response = client.get("/api/v1/auth/me")

    assert response.status_code == 401


# 6. Accessing profile with authentication
def test_get_me_authenticated(client):
    def mock_current_user():
        return {
            "_id": "123",
            "email": "test@example.com"
        }

    app.dependency_overrides[get_current_user] = mock_current_user

    try:
        response = client.get("/api/v1/auth/me")

        assert response.status_code == 200
        assert response.json() == {
            "id": "123",
            "email": "test@example.com"
        }
    finally:
        app.dependency_overrides.clear()


# 7. Successful logout
def test_logout_success(client):
    response = client.post("/api/v1/auth/logout")

    assert response.status_code == 200
    assert response.json()["message"] == "Logout successful"
    assert "access_token" in response.headers.get("set-cookie", "")
