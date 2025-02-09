from sqlmodel import SQLModel
from pydantic import Field
from typing import Optional


# ✅ JSON payload containing access & refresh tokens
class Token(SQLModel):
    access_token: str
    refresh_token: Optional[str] = None  # Can be None if just refreshing access token
    token_type: str = "bearer"


# ✅ JWT Token Payload (sent back to the frontend)
class TokenPayload(SQLModel):
    sub: str  # User email or user ID
    auth_provider: str = "local"  # 'local', 'google', 'facebook'


# ✅ Model for requesting access token refresh
class TokenRefreshRequest(SQLModel):
    refresh_token: str  # The refresh token must be provided


# ✅ Model for password reset
class NewPassword(SQLModel):
    token: str
    new_password: str = Field(min_length=8, max_length=40)


class RefreshTokenRequest(SQLModel):
    refresh_token: str


class LogoutRequest(SQLModel):
    refresh_token: str
