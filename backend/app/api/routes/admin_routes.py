from fastapi import APIRouter, Depends
from typing import Any
from uuid import UUID

from app.core.security.dependencies import get_current_active_superuser, SessionDep
from app.models import user, common
from app.services import user_service  # ✅ Import user management services

router = APIRouter()


# 🔹 ✅ Retrieve all users (Admin Only)
@router.get("/users", dependencies=[Depends(get_current_active_superuser)], response_model=user.UsersPublic, operation_id="get_all_users")
def read_users(session: SessionDep, skip: int = 0, limit: int = 100) -> Any:
    """Retrieve a list of all users (Admin only)."""
    return user_service.get_users(session, skip, limit)


# 🔹 ✅ Retrieve a specific user by ID (Admin Only)
@router.get("/users/detail/{user_id}", dependencies=[Depends(get_current_active_superuser)], response_model=user.UserPublic, operation_id="get_user_by_id")
def read_user_by_id(user_id: UUID, session: SessionDep) -> Any:
    """Retrieve details of a specific user by ID (Admin only)."""
    return user_service.get_user_by_id(session, user_id, None)


# 🔹 ✅ Create a new user (Admin Only)
@router.post("/users", dependencies=[Depends(get_current_active_superuser)], response_model=user.UserPublic, operation_id="create_user")
def create_user(session: SessionDep, user_in: user.UserCreate) -> Any:
    """Create a new user (Admin only)."""
    return user_service.create_user(session, user_in)


# 🔹 ✅ Update a user's details (Admin Only)
@router.patch("/users/{user_id}", dependencies=[Depends(get_current_active_superuser)], response_model=user.UserPublic, operation_id="update_user")
def update_user(session: SessionDep, user_id: UUID, user_in: user.UserUpdate) -> Any:
    """Update a user's details (Admin only)."""
    return user_service.update_user(session, user_id, user_in)


# 🔹 ✅ Delete a user (Admin Only)
@router.delete("/users/{user_id}", dependencies=[Depends(get_current_active_superuser)], response_model=common.Message, operation_id="delete_user")
def delete_user(session: SessionDep, user_id: UUID) -> common.Message:
    """Delete a user by ID (Admin only)."""
    return user_service.delete_user(session, user_id)
