from pydantic import Field
from sqlmodel import SQLModel


class Token(SQLModel):
    access_token: str
    refresh_token: str | None = None
    token_type: str = "bearer"


class TokenPayload(SQLModel):
    sub: str  # User email or user ID
    auth_provider: str = "local"  # 'local', 'google', 'facebook'


class TokenRefreshRequest(SQLModel):
    refresh_token: str


class NewPassword(SQLModel):
    token: str
    new_password: str = Field(min_length=8, max_length=40)


class RefreshTokenRequest(SQLModel):
    refresh_token: str


class LogoutRequest(SQLModel):
    refresh_token: str
