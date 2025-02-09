import uuid
from typing import Any

from sqlmodel import func, select

from app.core.utils.email import generate_new_account_email, send_email
from app.core.config.settings import settings
from fastapi import HTTPException
from sqlmodel import Session
from uuid import UUID
from app.models import user, common
from app.crud import crud_user


# ✅ Retrieve all users
def get_users(session, skip: int, limit: int) -> user.UsersPublic:
    count = session.exec(select(func.count()).select_from(user.User)).one()
    users = session.exec(select(user.User).offset(skip).limit(limit)).all()
    return user.UsersPublic(data=users, count=count)


# ✅ Create a new user
def create_user(session, user_in: user.UserCreate) -> Any:
    existing_user = crud_user.get_user_by_email(session=session, email=user_in.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists.")

    new_user = crud_user.create_user(session=session, user_create=user_in)

    if settings.emails_enabled and user_in.email:
        email_data = generate_new_account_email(
            email_to=user_in.email, username=user_in.email, password=user_in.password
        )
        send_email(email_to=user_in.email, subject=email_data.subject, html_content=email_data.html_content)

    return new_user


# ✅ Update current user profile
def update_user_profile(session, user_in: user.UserUpdateMe, current_user) -> Any:
    if user_in.email:
        existing_user = crud_user.get_user_by_email(session=session, email=user_in.email)
        if existing_user and existing_user.id != current_user.id:
            raise HTTPException(status_code=409, detail="User with this email already exists")

    current_user.sqlmodel_update(user_in.model_dump(exclude_unset=True))
    session.add(current_user)
    session.commit()
    session.refresh(current_user)
    return current_user


# ✅ Delete current user
def delete_self(session, current_user) -> Any:
    if current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Super users cannot delete themselves")

    session.delete(current_user)
    session.commit()
    return common.Message(message="User deleted successfully")


# ✅ Retrieve user by ID
def get_user_by_id(session, user_id: uuid.UUID, current_user) -> Any:
    user_instance = session.get(user.User, user_id)
    if not user_instance:
        raise HTTPException(status_code=404, detail="User not found")

    if user_instance == current_user or current_user.is_superuser:
        return user_instance

    raise HTTPException(status_code=403, detail="Insufficient privileges")


# ✅ Update a user's details
def update_user(session, user_id: uuid.UUID, user_in: user.UserUpdate) -> Any:
    db_user = session.get(user.User, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    if user_in.email:
        existing_user = crud_user.get_user_by_email(session=session, email=user_in.email)
        if existing_user and existing_user.id != user_id:
            raise HTTPException(status_code=409, detail="User with this email already exists")

    db_user = user.update_user(session=session, db_user=db_user, user_in=user_in)
    return db_user


# ✅ Delete a user
def delete_user(session, user_id: uuid.UUID) -> common.Message:
    user_instance = session.get(user.User, user_id)
    if not user_instance:
        raise HTTPException(status_code=404, detail="User not found")

    session.delete(user_instance)
    session.commit()
    return common.Message(message="User deleted successfully")


def register_user(session: Session, user_in: user.UserRegister) -> user.UserPublic:
    """Register a new user (Public signup)."""
    existing_user = crud_user.get_user_by_email(session=session, email=user_in.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists.")

    new_user = crud_user.create_user(session=session, user_create=user.UserCreate.model_validate(user_in))
    return new_user


def update_password(session: Session, user_id: UUID, old_password: str, new_password: str) -> common.Message:
    """Update user password after verifying the current password."""
    db_user = session.get(user.User, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    if not crud_user.authenticate(session=session, email=db_user.email, password=old_password):
        raise HTTPException(status_code=400, detail="Incorrect current password")

    updated_user = crud_user.update_user(session=session, db_user=db_user,
                                         user_in=user.UserUpdate(password=new_password))
    return common.Message(message="Password updated successfully")


def get_user_profile(session: Session, user_id: UUID) -> user.UserPublic:
    """Retrieve user profile."""
    db_user = session.get(user.User, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    return db_user
