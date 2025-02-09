import uuid
from typing import Optional
from pydantic import EmailStr
from sqlmodel import Field, SQLModel


# ✅ Define UserBase first
class UserBase(SQLModel):
    email: EmailStr = Field(unique=True, index=True, max_length=255)
    is_active: bool = True
    is_superuser: bool = False
    full_name: Optional[str] = Field(default=None, max_length=255)


# ✅ Define User model (Database Table)
class User(UserBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    hashed_password: Optional[str] = Field(default=None, max_length=255)  # Now nullable for social logins
    auth_provider: str = Field(default="local", max_length=50)  # 'local', 'google', 'facebook'
    provider_id: Optional[str] = Field(default=None, unique=True, max_length=255)  # Google/Facebook ID
    avatar_url: Optional[str] = Field(default=None, max_length=500)  # Profile picture


# ✅ User Creation (Normal Signup)
class UserCreate(UserBase):
    password: Optional[str] = Field(default=None, min_length=8, max_length=40)  # 🔴 Make password optional



# ✅ User Registration
class UserRegister(SQLModel):
    email: EmailStr = Field(max_length=255)
    password: str = Field(min_length=8, max_length=40)
    full_name: Optional[str] = Field(default=None, max_length=255)


# ✅ User Update (Admin)
class UserUpdate(UserBase):
    email: Optional[EmailStr] = Field(default=None, max_length=255)
    password: Optional[str] = Field(default=None, min_length=8, max_length=40)


# ✅ User Profile Update (Self)
class UserUpdateMe(SQLModel):
    full_name: Optional[str] = Field(default=None, max_length=255)
    email: Optional[EmailStr] = Field(default=None, max_length=255)


# ✅ Password Updates
class UpdatePassword(SQLModel):
    current_password: str = Field(min_length=8, max_length=40)
    new_password: str = Field(min_length=8, max_length=40)


class NewPassword(SQLModel):
    token: str
    new_password: str = Field(min_length=8, max_length=40)


# ✅ API Response Models
class UserPublic(UserBase):
    id: uuid.UUID
    auth_provider: str
    avatar_url: Optional[str] = None


class UsersPublic(SQLModel):
    data: list[UserPublic]
    count: int
