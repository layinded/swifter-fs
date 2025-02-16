from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, delete

from app.core.config.settings import settings
from app.core.database.database import engine
from app.core.database.db_setup import setup_database
from app.main import app
from app.models.user import User
from app.tests.utils.user import authentication_token_from_email
from app.tests.utils.utils import get_superuser_token_headers


@pytest.fixture(scope="session", autouse=True)
def db() -> Generator[Session, None, None]:
    """
    Set up the database session for the entire test session.
    Initializes the database schema and seeds initial data.
    After tests run, it cleans up by deleting Items and Users.
    """
    with Session(engine) as session:
        setup_database()
        yield session
        # Cleanup after tests: remove Items and Users
        session.execute(delete(User))
        session.commit()


@pytest.fixture(scope="module")
def client() -> Generator[TestClient, None, None]:
    """
    Creates a TestClient for the FastAPI app for module-level tests.
    """
    with TestClient(app) as c:
        yield c


@pytest.fixture(scope="module")
def superuser_token_headers(client: TestClient) -> dict[str, str]:
    """
    Returns authentication headers for a superuser.
    """
    return get_superuser_token_headers(client)


@pytest.fixture(scope="module")
def normal_user_token_headers(client: TestClient, db: Session) -> dict[str, str]:
    """
    Returns authentication headers for a normal test user using the test email from settings.
    """
    return authentication_token_from_email(
        client=client, email=settings.EMAIL_TEST_USER, db=db
    )
