import uuid

import pytest
from pydantic import ValidationError

from app.models.user import (
    NewPassword,
    UpdatePassword,
    User,
    UserBase,
    UserCreate,
    UserPublic,
    UserRegister,
    UsersPublic,
    UserUpdate,
    UserUpdateMe,
)


def test_user_base_valid():
    base = UserBase(
        email="user@example.com",
        full_name="Test User",
        is_active=True,
        is_superuser=False,
    )
    assert base.email == "user@example.com"
    assert base.full_name == "Test User"
    assert base.is_active is True
    assert base.is_superuser is False


def test_user_base_invalid_email():
    with pytest.raises(ValidationError):
        UserBase(email="not-an-email")


def test_user_creation_defaults():
    # Creating a User instance (table model) should generate a UUID and use defaults.
    user = User(
        email="user@example.com",
        full_name="Test User",
        hashed_password="hashed_password",
        auth_provider="local",
    )
    assert isinstance(user.id, uuid.UUID)
    assert user.email == "user@example.com"
    assert user.hashed_password == "hashed_password"
    # provider_id and avatar_url default to None.
    assert user.provider_id is None
    assert user.avatar_url is None


def test_user_create_optional_password():
    # In UserCreate, password is optional.
    user_create = UserCreate(email="user@example.com", full_name="Test User")
    assert user_create.password is None


def test_user_register_requires_password():
    # In UserRegister, password is required.
    with pytest.raises(ValidationError):
        UserRegister(email="user@example.com")
    user_reg = UserRegister(
        email="user@example.com", password="strongpwd", full_name="Test User"
    )
    assert user_reg.email == "user@example.com"
    assert user_reg.password == "strongpwd"


def test_user_update_optional_fields():
    # All fields in UserUpdate are optional.
    update = UserUpdate()
    assert update.email is None
    assert update.password is None
    # When provided, they should validate correctly.
    update2 = UserUpdate(email="new@example.com", password="newpassword")
    assert update2.email == "new@example.com"
    assert update2.password == "newpassword"


def test_user_update_me():
    update_me = UserUpdateMe(email="new@example.com", full_name="New Name")
    assert update_me.email == "new@example.com"
    assert update_me.full_name == "New Name"


def test_update_password_valid():
    update_pwd = UpdatePassword(
        current_password="oldpassword", new_password="newstrongpwd"
    )
    assert update_pwd.current_password == "oldpassword"
    assert update_pwd.new_password == "newstrongpwd"


def test_update_password_too_short():
    # Both current and new password must be at least 8 characters.
    with pytest.raises(ValidationError):
        UpdatePassword(current_password="short", new_password="short")


def test_new_password_valid():
    new_pwd = NewPassword(token="sometoken", new_password="validPassword")
    assert new_pwd.token == "sometoken"
    assert new_pwd.new_password == "validPassword"


def test_new_password_too_short():
    with pytest.raises(ValidationError):
        NewPassword(token="sometoken", new_password="short")


def test_user_public_conversion():
    base = UserBase(
        email="user@example.com",
        full_name="Test User",
        is_active=True,
        is_superuser=False,
    )
    user_public = UserPublic(
        **base.dict(), id=uuid.uuid4(), auth_provider="local", avatar_url=None
    )
    assert user_public.email == "user@example.com"
    assert user_public.auth_provider == "local"


def test_users_public():
    user1 = UserPublic(
        id=uuid.uuid4(),
        email="user1@example.com",
        full_name="User One",
        auth_provider="local",
    )
    user2 = UserPublic(
        id=uuid.uuid4(),
        email="user2@example.com",
        full_name="User Two",
        auth_provider="local",
    )
    users_public = UsersPublic(data=[user1, user2], count=2)
    assert users_public.count == 2
    assert len(users_public.data) == 2
