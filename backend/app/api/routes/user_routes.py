from typing import Any
from uuid import UUID

from fastapi import APIRouter, HTTPException

from app.core.security.dependencies import CurrentUser, SessionDep
from app.models import user
from app.services import user_service

router = APIRouter()


@router.patch("/me", response_model=user.UserPublic, operation_id="update_current_user")
def update_user_me(
    session: SessionDep, user_in: user.UserUpdateMe, current_user: CurrentUser
) -> Any:
    """Update the profile of the currently logged-in user."""
    return user_service.update_user_profile(session, user_in, current_user)


@router.get("/{user_id}", response_model=user.UserPublic, operation_id="get_user_by_id")
def read_user_by_id(
    user_id: UUID, session: SessionDep, current_user: CurrentUser
) -> Any:
    """Retrieve details of a user by ID (Only if it's the current user)."""
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Access denied")
    return user_service.get_user_by_id(session, user_id, current_user)
