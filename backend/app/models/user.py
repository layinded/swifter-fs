import uuid

from pydantic import EmailStr
from sqlalchemy import Column, String, text
from sqlmodel import Field, SQLModel


class UserBase(SQLModel):
    email: EmailStr = Field(unique=True, index=True, max_length=255)
    is_active: bool = True
    is_superuser: bool = False
    full_name: str | None = Field(default=None, max_length=255)
    # Set both the application-level default and the server-side default:
    preferred_language: str = Field(
        default="en", sa_column=Column(String(5), server_default=text("'en'"))
    )


class User(UserBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    hashed_password: str | None = Field(default=None, max_length=255)
    auth_provider: str = Field(default="local", max_length=50)
    provider_id: str | None = Field(default=None, unique=True, max_length=255)
    avatar_url: str | None = Field(default=None, max_length=500)


class UserCreate(UserBase):
    password: str | None = Field(default=None, min_length=8, max_length=40)


class UserRegister(SQLModel):
    email: EmailStr = Field(max_length=255)
    password: str = Field(min_length=8, max_length=40)
    full_name: str | None = Field(default=None, max_length=255)


class UserUpdate(UserBase):
    email: EmailStr | None = Field(default=None, max_length=255)
    password: str | None = Field(default=None, min_length=8, max_length=40)


class UserUpdateMe(SQLModel):
    full_name: str | None = Field(default=None, max_length=255)
    email: EmailStr | None = Field(default=None, max_length=255)
    preferred_language: str | None = Field(
        default=None, max_length=5
    )  # Added for user profile updates


class UpdatePassword(SQLModel):
    current_password: str = Field(min_length=8, max_length=40)
    new_password: str = Field(min_length=8, max_length=40)


class NewPassword(SQLModel):
    token: str
    new_password: str = Field(min_length=8, max_length=40)


class UserPublic(UserBase):
    id: uuid.UUID
    auth_provider: str
    avatar_url: str | None = None
    preferred_language: str


class UsersPublic(SQLModel):
    data: list[UserPublic]
    count: int
