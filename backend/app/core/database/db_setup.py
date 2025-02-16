import logging

from sqlmodel import Session, select
from tenacity import after_log, before_log, retry, stop_after_attempt, wait_fixed

from app.core.config.settings import settings
from app.core.database.database import SessionLocal
from app.crud.crud_user import create_user
from app.models.user import User, UserCreate

logger = logging.getLogger(__name__)


max_tries = 60 * 5  # 5 minutes max retry
wait_seconds = 1


@retry(
    stop=stop_after_attempt(max_tries),
    wait=wait_fixed(wait_seconds),
    before=before_log(logger, logging.INFO),
    after=after_log(logger, logging.WARN),
)
def check_db_ready() -> None:
    """Ensures the database is ready before starting services."""
    try:
        with SessionLocal() as session:
            session.exec(select(1))
    except Exception as e:
        logger.error(f"Database is not ready: {e}")
        raise e


def init_superuser(session: Session) -> None:
    """Ensures a superuser exists in the database."""
    superuser_email = settings.FIRST_SUPERUSER
    existing_user = session.exec(
        select(User).where(User.email == superuser_email)
    ).first()

    if not existing_user:
        user_in = UserCreate(
            email=superuser_email,
            password=settings.FIRST_SUPERUSER_PASSWORD,
            is_superuser=True,
        )
        create_user(session=session, user_create=user_in)
        session.commit()
        logger.info(f"Superuser '{superuser_email}' created.")
    else:
        logger.info("Superuser already exists. No changes made.")


def setup_database() -> None:
    """Main function to check DB readiness and create superuser."""
    logger.info("Checking database readiness...")
    check_db_ready()

    with SessionLocal() as session:
        init_superuser(session)

    logger.info("Database is ready and initialized!")


if __name__ == "__main__":
    setup_database()
