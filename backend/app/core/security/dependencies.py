import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from pydantic import ValidationError
from typing import Annotated
from sqlmodel import select

from app.core.security.refresh_token_service import ALGORITHM
from app.core.config.settings import settings
from app.models.auth import TokenPayload
from app.models.user import User
from app.core.database.dependencies import SessionDep

# ✅ OAuth2 Token Extraction
reusable_oauth2 = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/login")
TokenDep = Annotated[str, Depends(reusable_oauth2)]


def get_current_user(session: SessionDep, token: TokenDep) -> User:
    """
    Retrieve the current user from the JWT token.
    """
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
        token_data = TokenPayload(**payload)
    except (InvalidTokenError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )

    # ✅ Query user by email
    statement = select(User).where(User.email == token_data.sub)
    user = session.exec(statement).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")

    return user


# ✅ Dependency for retrieving the current authenticated user
CurrentUser = Annotated[User, Depends(get_current_user)]


def get_current_active_superuser(current_user: CurrentUser) -> User:
    """
    Ensure the user has superuser privileges.
    """
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The user doesn't have enough privileges",
        )
    return current_user


# ✅ Dynamic Role-Based Access Control
def require_roles(*roles):
    """
    Factory function to create a dependency that ensures the user has at least one of the required roles.

    Example:
        @router.get("/admin/dashboard", dependencies=[Depends(require_roles("admin", "superuser"))])
    """

    def role_checker(current_user: CurrentUser) -> User:
        if not any(getattr(current_user, role, False) for role in roles):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User lacks required privileges",
            )
        return current_user

    return role_checker
