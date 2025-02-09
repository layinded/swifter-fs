# Import SQLModel to ensure Alembic recognizes it
from sqlmodel import SQLModel  # ✅ Fix: Add this import

# Auto-load all models in `app/models/`
from app.models.user import User, UserCreate, UserUpdate, UserPublic, UsersPublic
from app.models.auth import Token, TokenPayload, NewPassword
from app.models.common import Message

# Ensure models are available for SQLAlchemy/Alembic
__all__ = [
    "SQLModel",  # ✅ Fix: Include SQLModel in __all__
    "User",
    "UserCreate",
    "UserUpdate",
    "UserPublic",
    "UsersPublic",
    "Token",
    "TokenPayload",
    "NewPassword",
    "Message",
]
