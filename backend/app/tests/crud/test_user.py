import uuid
import pytest
from datetime import datetime, timedelta, timezone
from unittest.mock import MagicMock, patch

from app.models.user import User, UserCreate, UserUpdate
from app.crud.crud_user import (
    create_user,
    update_user,
    get_user_by_email,
    authenticate,
    create_social_user,
)


# --- Helper: Dummy Session ---
class DummySession:
    def __init__(self):
        self.add_called = False
        self.commit_called = False
        self.refresh_called = False
        self.last_obj = None

    def add(self, obj):
        self.add_called = True
        self.last_obj = obj

    def commit(self):
        self.commit_called = True

    def refresh(self, obj):
        self.refresh_called = True
        return obj

    def exec(self, stmt):
        # For get_user_by_email, we simulate the .first() method.
        class DummyResult:
            def __init__(self, value):
                self.value = value

            def first(self):
                return self.value

        # The actual value will be patched in tests.
        return DummyResult(None)

    def get(self, model, id_):
        # This will be patched in tests if needed.
        return None


# --- Fake password security functions ---
def fake_get_password_hash(password: str) -> str:
    return f"hashed_{password}"


def fake_verify_password(password: str, hashed: str) -> bool:
    return hashed == f"hashed_{password}"


# --- Tests ---

# Test create_user for local accounts
@patch("app.crud.crud_user.get_password_hash", side_effect=fake_get_password_hash)
def test_create_user_local(mock_get_hash):
    session = DummySession()
    user_in = UserCreate(email="local@example.com", full_name="Local User", password="secret123")
    result = create_user(session=session, user_create=user_in, auth_provider="local")
    assert result.email == "local@example.com"
    assert result.full_name == "Local User"
    assert result.hashed_password == "hashed_secret123"
    assert result.auth_provider == "local"
    # Ensure session methods were called.
    assert session.add_called
    assert session.commit_called
    assert session.refresh_called


# Test create_user for social accounts (non-local)
@patch("app.crud.crud_user.get_password_hash")
def test_create_user_social(mock_get_hash):
    session = DummySession()
    # Use a valid dummy password that meets the minimum length requirement.
    user_in = UserCreate(email="social@example.com", full_name="Social User", password="ignored1")
    result = create_user(session=session, user_create=user_in, auth_provider="google")
    # For social logins, password is not hashed.
    assert result.email == "social@example.com"
    assert result.full_name == "Social User"
    assert result.hashed_password is None
    assert result.auth_provider == "google"



# Test update_user: updating password for a local user.
@patch("app.crud.crud_user.get_password_hash", side_effect=fake_get_password_hash)
def test_update_user_password(mock_get_hash):
    session = DummySession()
    # Create a dummy existing user.
    db_user = User(
        id=uuid.uuid4(),
        email="update@example.com",
        full_name="Old Name",
        auth_provider="local",
        hashed_password="hashed_oldpassword"
    )
    # Create a UserUpdate that includes a new password.
    user_in = UserUpdate(password="newsecret")
    updated = update_user(session=session, db_user=db_user, user_in=user_in)
    # Expect the hashed password to be updated.
    assert updated.hashed_password == "hashed_newsecret"
    assert session.add_called
    assert session.commit_called
    assert session.refresh_called


# Test update_user: updating fields without changing password.
def test_update_user_no_password():
    session = DummySession()
    db_user = User(
        id=uuid.uuid4(),
        email="update2@example.com",
        full_name="Old Name",
        auth_provider="local",
        hashed_password="hashed_oldpassword"
    )
    user_in = UserUpdate(full_name="New Name")
    updated = update_user(session=session, db_user=db_user, user_in=user_in)
    assert updated.full_name == "New Name"
    # Password remains unchanged.
    assert updated.hashed_password == "hashed_oldpassword"


def test_get_user_by_email_found():
    session = DummySession()
    dummy_user = User(
        id=uuid.uuid4(),
        email="found@example.com",
        full_name="Found User",
        auth_provider="local",
        hashed_password="hashed_secret"
    )
    # Patch session.exec() so that first() returns dummy_user.
    session.exec = lambda stmt: type("DummyResult", (), {"first": lambda _: dummy_user})()
    result = get_user_by_email(session=session, email="found@example.com")
    assert result == dummy_user



def test_get_user_by_email_not_found():
    session = DummySession()
    session.exec = lambda stmt: type("DummyResult", (), {"first": lambda _: None})()
    result = get_user_by_email(session=session, email="notfound@example.com")
    assert result is None


# Test authenticate: valid credentials for a local user.
@patch("app.crud.crud_user.verify_password", side_effect=fake_verify_password)
def test_authenticate_success(mock_verify):
    session = DummySession()
    dummy_user = User(
        id=uuid.uuid4(),
        email="auth@example.com",
        full_name="Auth User",
        auth_provider="local",
        hashed_password="hashed_secret123"
    )
    with patch("app.crud.crud_user.get_user_by_email", return_value=dummy_user):
        result = authenticate(session=session, email="auth@example.com", password="secret123")
        assert result == dummy_user


# Test authenticate: invalid password for a local user.
@patch("app.crud.crud_user.verify_password", side_effect=fake_verify_password)
def test_authenticate_invalid_password(mock_verify):
    session = DummySession()
    dummy_user = User(
        id=uuid.uuid4(),
        email="authfail@example.com",
        full_name="Auth Fail",
        auth_provider="local",
        hashed_password="hashed_secret123"
    )
    with patch("app.crud.crud_user.get_user_by_email", return_value=dummy_user):
        result = authenticate(session=session, email="authfail@example.com", password="wrongpassword")
        assert result is None


# Test authenticate: non-existent user.
def test_authenticate_nonexistent():
    session = DummySession()
    with patch("app.crud.crud_user.get_user_by_email", return_value=None):
        result = authenticate(session=session, email="nonexistent@example.com", password="any")
        assert result is None


# Test create_social_user: return existing user if already present.
def test_create_social_user_existing():
    session = DummySession()
    dummy_user = User(
        id=uuid.uuid4(),
        email="social@example.com",
        full_name="Social Existing",
        auth_provider="google"
    )
    with patch("app.crud.crud_user.get_user_by_email", return_value=dummy_user):
        user_info = {"sub": "google123", "name": "Social Existing"}
        result = create_social_user(session=session, email="social@example.com", user_info=user_info, provider="google")
        assert result == dummy_user


# Test create_social_user: create a new social user.
def test_create_social_user_new():
    session = DummySession()
    with patch("app.crud.crud_user.get_user_by_email", return_value=None):
        user_info = {"sub": "google456", "name": "Social New"}
        result = create_social_user(session=session, email="newsocial@example.com", user_info=user_info,
                                    provider="google")
        assert result.email == "newsocial@example.com"
        assert result.full_name == "Social New"
        assert result.auth_provider == "google"
        # The provider_id should be set from user_info["sub"].
        assert result.provider_id == "google456"


# Test create_social_user: missing provider id raises ValueError.
def test_create_social_user_missing_provider_id():
    session = DummySession()
    with patch("app.crud.crud_user.get_user_by_email", return_value=None):
        user_info = {"name": "No Provider ID"}
        with pytest.raises(ValueError) as exc_info:
            create_social_user(session=session, email="fail@example.com", user_info=user_info, provider="google")
        assert "Missing provider ID for google login" in str(exc_info.value)
