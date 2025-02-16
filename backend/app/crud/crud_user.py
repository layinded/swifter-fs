from typing import Any

from sqlmodel import Session, select

from app.core.security.password_security import get_password_hash, verify_password
from app.models.user import User, UserCreate, UserUpdate


def create_user(
    *,
    session: Session,
    user_create: UserCreate,
    auth_provider: str = "local",
    provider_id: str | None = None,
) -> User:
    """
    Create a new user with support for both local and social logins.
    """
    hashed_password = (
        get_password_hash(user_create.password) if auth_provider == "local" else None
    )

    db_obj = User.model_validate(
        user_create,
        update={
            "hashed_password": hashed_password,
            "auth_provider": auth_provider,
            "provider_id": provider_id,
        },
    )
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj


def update_user(*, session: Session, db_user: User, user_in: UserUpdate) -> Any:
    """Update user details, including password hashing if applicable."""
    user_data = user_in.model_dump(exclude_unset=True)
    extra_data = {}

    # Only hash password if updating a local user
    if "password" in user_data and db_user.auth_provider == "local":
        password = user_data["password"]
        hashed_password = get_password_hash(password)
        extra_data["hashed_password"] = hashed_password

    db_user.sqlmodel_update(user_data, update=extra_data)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


def get_user_by_email(*, session: Session, email: str) -> User | None:
    """Retrieve a user by email (for local and social logins)."""
    statement = select(User).where(User.email == email)
    return session.exec(statement).first()


def authenticate(*, session: Session, email: str, password: str) -> User | None:
    """Authenticate a user with email and password (only for local accounts)."""
    db_user = get_user_by_email(session=session, email=email)

    if not db_user:
        return None

    # Only check password if the user is a local user
    if db_user.auth_provider == "local":
        if not db_user.hashed_password or not verify_password(
            password, db_user.hashed_password
        ):
            return None

    return db_user


def create_social_user(
    session: Session, email: str, user_info: dict, provider: str
) -> User:
    """
    Create a new user from a social login (Google, Facebook, GitHub).
    """
    db_user = get_user_by_email(session=session, email=email)

    if db_user:
        return db_user

    if provider == "google":
        provider_id = user_info.get("sub")  # Google `sub`
    elif provider == "facebook":
        provider_id = user_info.get("id")  # Facebook `id'
    else:
        provider_id = None

    if not provider_id:
        raise ValueError(f"Missing provider ID for {provider} login")

    new_user = User(
        email=email,
        full_name=user_info.get("name"),
        provider_id=provider_id,
        auth_provider=provider,
        is_active=True,
    )

    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return new_user
