import uuid
from datetime import datetime, timezone

from sqlmodel import Field, SQLModel


class RefreshToken(SQLModel, table=True):
    """
    Stores refresh tokens linked to users.
    - Each user has **only one refresh token** at a time.
    - Refresh token is updated instead of creating new entries.
    """

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_email: str = Field(index=True)
    token: str = Field(..., nullable=False)  # Mark token as required
    expires_at: datetime = Field(nullable=False)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
