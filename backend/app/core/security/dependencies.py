from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from pydantic import ValidationError
from sqlmodel import select

from app.core.config.settings import settings
from app.core.database.dependencies import SessionDep
from app.core.security.refresh_token_service import ALGORITHM
from app.core.utils.translation_helper import translate
from app.models.auth import TokenPayload
from app.models.user import User

reusable_oauth2 = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/login")
TokenDep = Annotated[str, Depends(reusable_oauth2)]


def get_current_user(session: SessionDep, token: TokenDep, request: Request) -> User:
    """
    Retrieve the current user from the JWT token.
    """
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
        token_data = TokenPayload(**payload)
    except (InvalidTokenError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=translate(request, "could_not_validate_credentials"),
        )
    statement = select(User).where(User.email == token_data.sub)
    user = session.exec(statement).first()
    if not user:
        raise HTTPException(
            status_code=404, detail=translate(request, "user_not_found")
        )
    if not user.is_active:
        raise HTTPException(status_code=400, detail=translate(request, "inactive_user"))
    return user


CurrentUser = Annotated[User, Depends(get_current_user)]


def get_current_active_superuser(current_user: CurrentUser, request: Request) -> User:
    """
    Ensure the user has superuser privileges.
    """
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=translate(request, "insufficient_privileges"),
        )
    return current_user


def require_roles(*roles):
    """
    Factory function to create a dependency that ensures the user has at least one of the required roles.

    Example:
        @router.get("/admin/dashboard", dependencies=[Depends(require_roles("admin", "superuser"))])
    """

    def role_checker(current_user: CurrentUser, request: Request) -> User:
        if not any(getattr(current_user, role, False) for role in roles):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=translate(request, "user_lacks_required_privileges"),
            )
        return current_user

    return role_checker
