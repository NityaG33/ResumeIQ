
import pytest
import jwt
from datetime import timedelta

from auth.jwt import create_access_token, decode_access_token


def test_jwt_creation_and_decoding():
    token = create_access_token({"sub": "user123"})

    payload = decode_access_token(token)

    assert payload["sub"] == "user123"
    assert "exp" in payload


def test_jwt_with_custom_expiration():
    token = create_access_token(
        {"sub": "user123"},
        expires_delta=timedelta(minutes=30)
    )

    payload = decode_access_token(token)

    assert payload["sub"] == "user123"


def test_expired_jwt():
    token = create_access_token(
        {"sub": "user123"},
        expires_delta=timedelta(seconds=-1)
    )

    with pytest.raises(jwt.ExpiredSignatureError):
        decode_access_token(token)


def test_invalid_jwt():
    with pytest.raises(jwt.InvalidTokenError):
        decode_access_token("invalid.token.value")
