import uuid
from datetime import datetime, timedelta, timezone
from unittest.mock import MagicMock, patch
import pytest
from fastapi import HTTPException
from sqlmodel import Session

# Import the endpoints to be tested.
# Adjust the module path as needed.
from app.api import user_endpoints
from app.models import user, common


# --- get_users ---

def test_get_users():
    # Create dummy data: a single user and a count.
    dummy_user = user.User(
        id=uuid.uuid4(),
        email="user@example.com",
        full_name="User Example",
        auth_provider="local",
    )
    dummy_users = [dummy_user]
    dummy_count = 1

    # Create a fake session (MagicMock) with mocked exec() method.
    session = MagicMock(spec=Session)
    # Patch the chain: session.exec(...).one() returns dummy_count.
    session.exec.return_value.one.return_value = dummy_count
    # And session.exec(...).all() returns dummy_users.
    session.exec.return_value.all.return_value = dummy_users

    result = user_endpoints.get_users(session, skip=0, limit=10)
    assert result.count == dummy_count
    assert result.data == dummy_users


# --- create_user ---

def test_create_user_success():
    session = MagicMock(spec=Session)
    user_in = user.UserCreate(
        email="new@example.com",
        full_name="New User",
        password="strongpassword",
    )
    # Simulate no existing user.
    with patch("app.api.user_endpoints.crud_user.get_user_by_email", return_value=None) as mock_get:
        # Simulate successful user creation.
        dummy_user = user.User(
            id=uuid.uuid4(),
            email=user_in.email,
            full_name=user_in.full_name,
            auth_provider="local",
        )
        with patch("app.api.user_endpoints.crud_user.create_user", return_value=dummy_user) as mock_create:
            # Patch email functions if emails are enabled.
            with patch("app.api.user_endpoints.generate_new_account_email") as mock_generate_email:
                with patch("app.api.user_endpoints.send_email") as mock_send_email:
                    # Set up a dummy email payload.
                    email_data = type("EmailData", (), {"subject": "Welcome", "html_content": "<p>Hello</p>"})
                    mock_generate_email.return_value = email_data()

                    result = user_endpoints.create_user(session, user_in)
                    assert result == dummy_user
                    mock_get.assert_called_once_with(session=session, email=user_in.email)
                    mock_create.assert_called_once()
                    if user_endpoints.settings.emails_enabled and user_in.email:
                        mock_generate_email.assert_called_once()
                        mock_send_email.assert_called_once()


def test_create_user_existing():
    session = MagicMock(spec=Session)
    # Simulate that an existing user is found.
    existing_user = user.User(
        id=uuid.uuid4(), email="existing@example.com", full_name="Existing", auth_provider="local"
    )
    with patch("app.api.user_endpoints.crud_user.get_user_by_email", return_value=existing_user):
        user_in = user.UserCreate(
            email="existing@example.com", full_name="Existing", password="strongpassword"
        )
        with pytest.raises(HTTPException) as exc_info:
            user_endpoints.create_user(session, user_in)
        assert exc_info.value.status_code == 400


# --- update_user_profile ---

def test_update_user_profile_success():
    session = MagicMock(spec=Session)
    # Create a dummy current user.
    current_user = MagicMock(spec=user.User)
    current_user.id = uuid.uuid4()
    # Patch get_user_by_email to simulate no conflict.
    with patch("app.api.user_endpoints.crud_user.get_user_by_email", return_value=None):
        user_in = user.UserUpdateMe(email="updated@example.com", full_name="Updated Name")

        # Simulate the model update function.
        def fake_update(data):
            current_user.email = data.get("email", current_user.email)
            current_user.full_name = data.get("full_name", current_user.full_name)

        current_user.sqlmodel_update = fake_update
        # Simulate session.refresh.
        session.refresh = lambda u: u

        result = user_endpoints.update_user_profile(session, user_in, current_user)
        assert result.email == "updated@example.com"
        assert result.full_name == "Updated Name"


def test_update_user_profile_conflict():
    session = MagicMock(spec=Session)
    current_user = MagicMock(spec=user.User)
    current_user.id = uuid.uuid4()
    # Simulate that another user exists with the target email.
    other_user = MagicMock(spec=user.User)
    other_user.id = uuid.uuid4()
    with patch("app.api.user_endpoints.crud_user.get_user_by_email", return_value=other_user):
        user_in = user.UserUpdateMe(email="conflict@example.com")
        with pytest.raises(HTTPException) as exc_info:
            user_endpoints.update_user_profile(session, user_in, current_user)
        assert exc_info.value.status_code == 409


# --- delete_self ---

def test_delete_self_non_superuser():
    session = MagicMock(spec=Session)
    current_user = MagicMock(spec=user.User)
    current_user.is_superuser = False
    result = user_endpoints.delete_self(session, current_user)
    assert isinstance(result, common.Message)
    assert result.message == "User deleted successfully"
    session.delete.assert_called_once_with(current_user)
    session.commit.assert_called_once()


def test_delete_self_superuser():
    session = MagicMock(spec=Session)
    current_user = MagicMock(spec=user.User)
    current_user.is_superuser = True
    with pytest.raises(HTTPException) as exc_info:
        user_endpoints.delete_self(session, current_user)
    assert exc_info.value.status_code == 403


# --- get_user_by_id ---

def test_get_user_by_id_not_found():
    session = MagicMock(spec=Session)
    session.get.return_value = None
    current_user = MagicMock(spec=user.User)
    current_user.id = uuid.uuid4()
    with pytest.raises(HTTPException) as exc_info:
        user_endpoints.get_user_by_id(session, uuid.uuid4(), current_user)
    assert exc_info.value.status_code == 404


def test_get_user_by_id_insufficient_privileges():
    session = MagicMock(spec=Session)
    other_user = MagicMock(spec=user.User)
    other_user.id = uuid.uuid4()
    session.get.return_value = other_user
    current_user = MagicMock(spec=user.User)
    current_user.id = uuid.uuid4()
    current_user.is_superuser = False
    with pytest.raises(HTTPException) as exc_info:
        user_endpoints.get_user_by_id(session, other_user.id, current_user)
    assert exc_info.value.status_code == 403


def test_get_user_by_id_success():
    session = MagicMock(spec=Session)
    dummy_user = MagicMock(spec=user.User)
    dummy_user.id = uuid.uuid4()
    session.get.return_value = dummy_user
    current_user = MagicMock(spec=user.User)
    current_user.id = dummy_user.id
    result = user_endpoints.get_user_by_id(session, dummy_user.id, current_user)
    assert result == dummy_user


# --- update_user ---

def test_update_user_not_found():
    session = MagicMock(spec=Session)
    session.get.return_value = None
    with pytest.raises(HTTPException) as exc_info:
        user_endpoints.update_user(session, uuid.uuid4(), user.UserUpdate(email="update@example.com"))
    assert exc_info.value.status_code == 404


def test_update_user_conflict():
    session = MagicMock(spec=Session)
    db_user = MagicMock(spec=user.User)
    db_user.id = uuid.uuid4()
    session.get.return_value = db_user
    other_user = MagicMock(spec=user.User)
    other_user.id = uuid.uuid4()
    with patch("app.api.user_endpoints.crud_user.get_user_by_email", return_value=other_user):
        with pytest.raises(HTTPException) as exc_info:
            user_endpoints.update_user(session, db_user.id, user.UserUpdate(email="conflict@example.com"))
        assert exc_info.value.status_code == 409


def test_update_user_success():
    session = MagicMock(spec=Session)
    db_user = MagicMock(spec=user.User)
    db_user.id = uuid.uuid4()
    session.get.return_value = db_user
    update_data = user.UserUpdate(email="updated@example.com", password="newpassword")
    with patch("app.api.user_endpoints.crud_user.update_user", return_value=db_user) as mock_update:
        result = user_endpoints.update_user(session, db_user.id, update_data)
        mock_update.assert_called_once()
        assert result == db_user


# --- delete_user ---

def test_delete_user_not_found():
    session = MagicMock(spec=Session)
    session.get.return_value = None
    with pytest.raises(HTTPException) as exc_info:
        user_endpoints.delete_user(session, uuid.uuid4())
    assert exc_info.value.status_code == 404


def test_delete_user_success():
    session = MagicMock(spec=Session)
    dummy_user = MagicMock(spec=user.User)
    dummy_user.id = uuid.uuid4()
    session.get.return_value = dummy_user
    result = user_endpoints.delete_user(session, dummy_user.id)
    assert isinstance(result, common.Message)
    assert result.message == "User deleted successfully"
    session.delete.assert_called_once_with(dummy_user)
    session.commit.assert_called_once()


# --- register_user ---

def test_register_user_success():
    session = MagicMock(spec=Session)
    with patch("app.api.user_endpoints.crud_user.get_user_by_email", return_value=None):
        dummy_user = MagicMock(spec=user.User)
        with patch("app.api.user_endpoints.crud_user.create_user", return_value=dummy_user):
            user_in = user.UserRegister(email="register@example.com", password="strongpassword",
                                        full_name="Register User")
            result = user_endpoints.register_user(session, user_in)
            assert result == dummy_user


def test_register_user_exists():
    session = MagicMock(spec=Session)
    dummy_user = MagicMock(spec=user.User)
    with patch("app.api.user_endpoints.crud_user.get_user_by_email", return_value=dummy_user):
        user_in = user.UserRegister(email="register@example.com", password="strongpassword", full_name="Register User")
        with pytest.raises(HTTPException) as exc_info:
            user_endpoints.register_user(session, user_in)
        assert exc_info.value.status_code == 400


# --- update_password ---

def test_update_password_incorrect():
    session = MagicMock(spec=Session)
    db_user = MagicMock(spec=user.User)
    db_user.email = "user@example.com"
    session.get.return_value = db_user
    with patch("app.api.user_endpoints.crud_user.authenticate", return_value=False):
        with pytest.raises(HTTPException) as exc_info:
            user_endpoints.update_password(session, uuid.uuid4(), "wrongpassword", "newpassword")
        assert exc_info.value.status_code == 400


def test_update_password_success():
    session = MagicMock(spec=Session)
    db_user = MagicMock(spec=user.User)
    db_user.email = "user@example.com"
    session.get.return_value = db_user
    with patch("app.api.user_endpoints.crud_user.authenticate", return_value=True):
        with patch("app.api.user_endpoints.crud_user.update_user", return_value=db_user) as mock_update:
            result = user_endpoints.update_password(session, db_user.id, "oldpassword", "newpassword")
            mock_update.assert_called_once()
            assert isinstance(result, common.Message)
            assert result.message == "Password updated successfully"


# --- get_user_profile ---

def test_get_user_profile_not_found():
    session = MagicMock(spec=Session)
    session.get.return_value = None
    with pytest.raises(HTTPException) as exc_info:
        user_endpoints.get_user_profile(session, uuid.uuid4())
    assert exc_info.value.status_code == 404


def test_get_user_profile_success():
    session = MagicMock(spec=Session)
    dummy_user = MagicMock(spec=user.User)
    dummy_user.id = uuid.uuid4()
    session.get.return_value = dummy_user
    result = user_endpoints.get_user_profile(session, dummy_user.id)
    assert result == dummy_user
