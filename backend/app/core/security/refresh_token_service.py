from datetime import datetime, timedelta, timezone
from typing import Optional, Tuple
import jwt
from fastapi import HTTPException
from sqlmodel import Session, select
from app.models.token import RefreshToken
from app.core.config.settings import settings

# ✅ JWT Algorithm
ALGORITHM = "HS256"


def create_access_token(email: str, expires_delta: timedelta, auth_provider: str = "local") -> str:
    """
    Generate a short-lived JWT access token.
    """
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode = {"exp": expire.timestamp(), "sub": email, "auth_provider": auth_provider}  # ✅ Store auth_provider
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)


def create_refresh_token(session: Session, email: str, expires_delta: timedelta, auth_provider: str = "local") -> str:
    """
    Create or update a refresh token for the user.
    - If a refresh token exists, update it instead of creating a new one.
    - If none exists, create a new one.
    """
    expire_at = datetime.now(timezone.utc) + expires_delta
    encoded_jwt = jwt.encode(
        {"exp": expire_at.timestamp(), "sub": email, "auth_provider": auth_provider},  # ✅ Store auth_provider
        settings.REFRESH_SECRET_KEY,
        algorithm=ALGORITHM
    )

    # 🔍 Check if a refresh token already exists
    existing_token = session.exec(select(RefreshToken).where(RefreshToken.user_email == email)).first()

    if existing_token:
        # ✅ Update existing refresh token
        existing_token.token = encoded_jwt
        existing_token.expires_at = expire_at
    else:
        # 🆕 Create a new refresh token if none exists
        new_refresh_token = RefreshToken(user_email=email, token=encoded_jwt, expires_at=expire_at)
        session.add(new_refresh_token)

    session.commit()
    return encoded_jwt


def verify_refresh_token(session: Session, refresh_token: str) -> Optional[Tuple[str, str]]:
    """
    Verify the refresh token and return (email, auth_provider) if valid.
    """
    try:
        print(f"🔍 Decoding refresh token: {refresh_token}")  # ✅ Debug log

        # 🔍 Decode JWT refresh token
        payload = jwt.decode(refresh_token, settings.REFRESH_SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        auth_provider = payload.get("auth_provider", "local")

        print(f"✅ Decoded JWT payload: {payload}")  # ✅ Debug log

        if not email:
            print("❌ Invalid token: Missing email")
            raise HTTPException(status_code=401, detail="Invalid refresh token payload")

        # 🔍 Validate token in DB
        db_token = session.exec(select(RefreshToken).where(RefreshToken.token == refresh_token)).first()
        if not db_token:
            print("❌ Refresh token not found in database!")
            raise HTTPException(status_code=401, detail="Invalid or revoked refresh token")

        if datetime.now(timezone.utc) > db_token.expires_at:
            print(f"❌ Refresh token expired! Expiration: {db_token.expires_at}")
            raise HTTPException(status_code=401, detail="Refresh token expired")

        print(f"✅ Refresh token is valid for user: {email}, Provider: {auth_provider}")
        return email, auth_provider

    except jwt.ExpiredSignatureError:
        print("❌ JWT Expired - Returning 401 Unauthorized")
        raise HTTPException(status_code=401, detail="Refresh token expired")

    except jwt.InvalidTokenError as e:
        print(f"❌ Invalid JWT Token: {str(e)}")
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    except Exception as e:
        print(f"❌ Unexpected Error in `verify_refresh_token`: {str(e)}")
        raise HTTPException(status_code=401, detail="Invalid or revoked refresh token")


def revoke_refresh_token(session: Session, refresh_token: str) -> bool:
    """
    Revoke a refresh token (logout).
    """
    db_token = session.exec(select(RefreshToken).where(RefreshToken.token == refresh_token)).first()
    if db_token:
        session.delete(db_token)
        session.commit()
        return True
    return False


def revoke_all_tokens(session: Session, email: str) -> None:
    """
    Revoke all refresh tokens for a user (e.g., on password reset).
    """
    db_tokens = session.exec(select(RefreshToken).where(RefreshToken.user_email == email)).all()
    for token in db_tokens:
        session.delete(token)
    session.commit()
