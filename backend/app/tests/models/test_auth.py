import pytest
from pydantic import ValidationError
from sqlmodel import SQLModel

# Import your models; adjust the import path as necessary.
from app.models.auth import (
    Token,
    TokenPayload,
    TokenRefreshRequest,
    NewPassword,
    RefreshTokenRequest,
    LogoutRequest,
)


def test_token_model_defaults():
    # When only the required field is provided
    token = Token(access_token="abc123")
    assert token.access_token == "abc123"
    assert token.refresh_token is None
    # token_type defaults to "bearer"
    assert token.token_type == "bearer"


def test_token_payload_defaults():
    # Only the 'sub' field is required; auth_provider should default to "local"
    payload = TokenPayload(sub="user@example.com")
    assert payload.sub == "user@example.com"
    assert payload.auth_provider == "local"


def test_token_refresh_request():
    refresh_req = TokenRefreshRequest(refresh_token="refresh123")
    assert refresh_req.refresh_token == "refresh123"


def test_new_password_valid():
    # This should pass as the new_password length is between 8 and 40 characters.
    new_pass = NewPassword(token="sometoken", new_password="validPass123")
    assert new_pass.token == "sometoken"
    assert new_pass.new_password == "validPass123"


def test_new_password_too_short():
    # A new_password with less than 8 characters should raise a validation error.
    with pytest.raises(ValidationError):
        NewPassword(token="sometoken", new_password="short")


def test_new_password_too_long():
    # A new_password longer than 40 characters should raise a validation error.
    long_password = "x" * 41
    with pytest.raises(ValidationError):
        NewPassword(token="sometoken", new_password=long_password)


def test_refresh_token_request_model():
    req = RefreshTokenRequest(refresh_token="refresh456")
    assert req.refresh_token == "refresh456"


def test_logout_request_model():
    req = LogoutRequest(refresh_token="logout789")
    assert req.refresh_token == "logout789"
