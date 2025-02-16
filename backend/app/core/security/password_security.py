from datetime import datetime, timedelta, timezone

import jwt
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
from passlib.context import CryptContext

from app.core.config.settings import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


ALGORITHM = "HS256"


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plaintext password against a hashed password."""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Hash a password using bcrypt."""
    return pwd_context.hash(password)


def generate_password_reset_token(
    email: str, auth_provider: str = "local"
) -> str | None:
    """
    Generate a JWT token for password reset.
    - Only available for users with `auth_provider = local`.
    """
    if auth_provider != "local":
        return None  # Social login users should reset passwords via their provider.

    expires = datetime.now(timezone.utc) + timedelta(
        hours=settings.EMAIL_RESET_TOKEN_EXPIRE_HOURS
    )

    encoded_jwt = jwt.encode(
        {"exp": expires.timestamp(), "sub": email, "auth_provider": "local"},
        settings.SECRET_KEY,
        algorithm=ALGORITHM,
    )
    return encoded_jwt


def verify_password_reset_token(token: str) -> str | None:
    """
    Verify and decode a password reset token.
    - Returns `None` if the token is invalid or expired.
    """
    try:
        decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
        if datetime.now(timezone.utc).timestamp() > decoded_token["exp"]:
            return None  # Token expired

        return str(decoded_token["sub"])

    except (ExpiredSignatureError, InvalidTokenError):
        return None  # Invalid or expired token
