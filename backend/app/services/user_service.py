import uuid
from typing import Any
from uuid import UUID

from fastapi import HTTPException, Request
from sqlmodel import Session, func, select

from app.core.config.settings import settings
from app.core.utils.email import generate_new_account_email, send_email
from app.core.utils.translation_helper import (
    translate,  # <-- Use the translation helper
)
from app.crud import crud_user
from app.models import common, user

# -----------------------------
# User Service Functions
# -----------------------------


def get_users(session: Session, skip: int, limit: int) -> user.UsersPublic:
    count = session.exec(select(func.count()).select_from(user.User)).one()
    users = session.exec(select(user.User).offset(skip).limit(limit)).all()
    return user.UsersPublic(data=users, count=count)


def create_user(
    session: Session, user_in: user.UserCreate, request: Request = None
) -> Any:
    existing_user = crud_user.get_user_by_email(session=session, email=user_in.email)
    if existing_user:
        raise HTTPException(
            status_code=400, detail=translate(request, "user_already_exists")
        )

    new_user = crud_user.create_user(session=session, user_create=user_in)

    if settings.emails_enabled and user_in.email:
        email_data = generate_new_account_email(
            email_to=user_in.email, username=user_in.email, password=user_in.password
        )
        send_email(
            email_to=user_in.email,
            subject=email_data.subject,
            html_content=email_data.html_content,
        )

    return new_user


def update_user_profile(
    session: Session, user_in: user.UserUpdateMe, current_user, request: Request = None
) -> Any:
    if user_in.email:
        existing_user = crud_user.get_user_by_email(
            session=session, email=user_in.email
        )
        if existing_user and existing_user.id != current_user.id:
            raise HTTPException(
                status_code=409, detail=translate(request, "user_email_already_exists")
            )

    current_user.sqlmodel_update(user_in.model_dump(exclude_unset=True))
    session.add(current_user)
    session.commit()
    session.refresh(current_user)
    return current_user


def delete_self(session: Session, current_user, request: Request = None) -> Any:
    if current_user.is_superuser:
        raise HTTPException(
            status_code=403, detail=translate(request, "superuser_cannot_delete")
        )

    session.delete(current_user)
    session.commit()
    return common.Message(message=translate(request, "user_deleted_successfully"))


def get_user_by_id(
    session: Session, user_id: uuid.UUID, current_user, request: Request = None
) -> Any:
    user_instance = session.get(user.User, user_id)
    if not user_instance:
        raise HTTPException(
            status_code=404, detail=translate(request, "user_not_found")
        )

    if user_instance == current_user or current_user.is_superuser:
        return user_instance

    raise HTTPException(
        status_code=403, detail=translate(request, "insufficient_privileges")
    )


def update_user(
    session: Session,
    user_id: uuid.UUID,
    user_in: user.UserUpdate,
    request: Request = None,
) -> Any:
    db_user = session.get(user.User, user_id)
    if not db_user:
        raise HTTPException(
            status_code=404, detail=translate(request, "user_not_found")
        )

    if user_in.email:
        existing_user = crud_user.get_user_by_email(
            session=session, email=user_in.email
        )
        if existing_user and existing_user.id != user_id:
            raise HTTPException(
                status_code=409, detail=translate(request, "user_email_already_exists")
            )

    db_user = crud_user.update_user(session=session, db_user=db_user, user_in=user_in)
    return db_user


def delete_user(
    session: Session, user_id: uuid.UUID, request: Request = None
) -> common.Message:
    user_instance = session.get(user.User, user_id)
    if not user_instance:
        raise HTTPException(
            status_code=404, detail=translate(request, "user_not_found")
        )

    session.delete(user_instance)
    session.commit()
    return common.Message(message=translate(request, "user_deleted_successfully"))


def register_user(
    session: Session, user_in: user.UserRegister, request: Request = None
) -> user.UserPublic:
    """Register a new user (Public signup)."""
    existing_user = crud_user.get_user_by_email(session=session, email=user_in.email)
    if existing_user:
        raise HTTPException(
            status_code=400, detail=translate(request, "user_already_exists")
        )

    new_user = crud_user.create_user(
        session=session, user_create=user.UserCreate.model_validate(user_in)
    )
    return new_user


def update_password(
    session: Session,
    user_id: UUID,
    old_password: str,
    new_password: str,
    request: Request = None,
) -> common.Message:
    """Update user password after verifying the current password."""
    db_user = session.get(user.User, user_id)
    if not db_user:
        raise HTTPException(
            status_code=404, detail=translate(request, "user_not_found")
        )

    if not crud_user.authenticate(
        session=session, email=db_user.email, password=old_password
    ):
        raise HTTPException(
            status_code=400, detail=translate(request, "incorrect_current_password")
        )

    crud_user.update_user(
        session=session, db_user=db_user, user_in=user.UserUpdate(password=new_password)
    )
    return common.Message(message=translate(request, "password_updated_successfully"))


def get_user_profile(
    session: Session, user_id: UUID, request: Request = None
) -> user.UserPublic:
    """Retrieve user profile."""
    db_user = session.get(user.User, user_id)
    if not db_user:
        raise HTTPException(
            status_code=404, detail=translate(request, "user_not_found")
        )

    return db_user
