from datetime import datetime, timedelta, timezone
from typing import Optional, Tuple
import jwt
from fastapi import HTTPException
from sqlmodel import Session, select
from app.models.token import RefreshToken
from app.core.config.settings import settings

ALGORITHM = "HS256"


def create_access_token(email: str, expires_delta: timedelta, auth_provider: str = "local") -> str:
    """
    Generate a short-lived JWT access token.
    """
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode = {
        "exp": expire.timestamp(),
        "sub": email,
        "auth_provider": auth_provider
    }
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)


def create_refresh_token(session: Session, email: str, expires_delta: timedelta, auth_provider: str = "local") -> str:
    """
    Create or update a refresh token for the user.
    - If a refresh token exists, update it instead of creating a new one.
    - If none exists, create a new one.
    """
    expire_at = datetime.now(timezone.utc) + expires_delta
    encoded_jwt = jwt.encode(
        {
            "exp": expire_at.timestamp(),
            "sub": email,
            "auth_provider": auth_provider
        },
        settings.REFRESH_SECRET_KEY,
        algorithm=ALGORITHM
    )

    # Check if a refresh token already exists for this user
    existing_token = session.exec(
        select(RefreshToken).where(RefreshToken.user_email == email)
    ).first()

    if existing_token:
        # Update existing refresh token
        existing_token.token = encoded_jwt
        existing_token.expires_at = expire_at
    else:
        # Create a new refresh token record
        new_refresh_token = RefreshToken(user_email=email, token=encoded_jwt, expires_at=expire_at)
        session.add(new_refresh_token)

    session.commit()
    return encoded_jwt


def verify_refresh_token(session: Session, refresh_token: str) -> Optional[Tuple[str, str]]:
    """
    Verify the refresh token and return (email, auth_provider) if valid.
    """
    try:
        print(f"🔍 Decoding refresh token: {refresh_token}")

        # Decode the JWT refresh token using the REFRESH_SECRET_KEY
        payload = jwt.decode(refresh_token, settings.REFRESH_SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        auth_provider = payload.get("auth_provider", "local")
        print(f"✅ Decoded JWT payload: {payload}")

        if not email:
            print("❌ Invalid token: Missing email")
            raise HTTPException(status_code=401, detail="Invalid refresh token payload")

        # Validate that the token exists in the database
        db_token = session.exec(
            select(RefreshToken).where(RefreshToken.token == refresh_token)
        ).first()
        if not db_token:
            print("❌ Refresh token not found in database!")
            raise HTTPException(status_code=401, detail="Invalid or revoked refresh token")

        # Ensure db_token.expires_at is timezone-aware (assume UTC if naive)
        token_exp = db_token.expires_at
        if token_exp.tzinfo is None:
            token_exp = token_exp.replace(tzinfo=timezone.utc)

        # Compare current time (timezone-aware) with token expiration
        if datetime.now(timezone.utc) > token_exp:
            print(f"❌ Refresh token expired! Expiration: {token_exp}")
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
    If the token is not found in the database, treat it as already revoked.
    """
    db_token = session.exec(
        select(RefreshToken).where(RefreshToken.token == refresh_token)
    ).first()
    if db_token:
        session.delete(db_token)
        session.commit()
        print("✅ Refresh token revoked.")
    else:
        print("⚠️ Refresh token not found in database (already revoked?)")
    # Return True regardless to indicate that the token is no longer valid
    return True


def revoke_all_tokens(session: Session, email: str) -> None:
    """
    Revoke all refresh tokens for a user (e.g., on password reset).
    """
    db_tokens = session.exec(
        select(RefreshToken).where(RefreshToken.user_email == email)
    ).all()
    for token in db_tokens:
        session.delete(token)
    session.commit()
    print(f"✅ All refresh tokens revoked for user: {email}")
