import uuid
from datetime import datetime, timedelta, timezone
import pytest
from pydantic import ValidationError

# Adjust the import path to match your project structure
from app.models.token import RefreshToken


def test_refresh_token_defaults():
    user_email = "user@example.com"
    token = "sometoken"
    expires_at = datetime.now(timezone.utc) + timedelta(days=1)

    refresh_token = RefreshToken(user_email=user_email, token=token, expires_at=expires_at)

    # Check that an id was automatically generated and is a valid UUID
    assert isinstance(refresh_token.id, uuid.UUID)

    # Verify that the provided values are correctly set
    assert refresh_token.user_email == user_email
    assert refresh_token.token == token
    assert refresh_token.expires_at == expires_at

    # Verify that created_at is set to a datetime with timezone info,
    # and that it is recent (within a few seconds of now)
    now = datetime.now(timezone.utc)
    delta = now - refresh_token.created_at
    assert delta.total_seconds() < 5
    assert refresh_token.created_at.tzinfo is not None


def test_refresh_token_missing_token():
    user_email = "user@example.com"
    expires_at = datetime.now(timezone.utc) + timedelta(days=1)

    # token is required, so missing it should raise a validation error
    with pytest.raises(ValidationError):
        RefreshToken.model_validate({
            "user_email": user_email,
            "expires_at": expires_at  # token missing
        })


def test_refresh_token_missing_expires_at():
    user_email = "user@example.com"
    token = "sometoken"

    # expires_at is required, so missing it should raise a validation error.
    with pytest.raises(ValidationError):
        # Use model_validate to enforce validation.
        RefreshToken.model_validate({
            "user_email": user_email,
            "token": token
        })
