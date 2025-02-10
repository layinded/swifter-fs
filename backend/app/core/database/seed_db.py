import logging
import sys
from sqlmodel import Session
from app.core.database.database import SessionLocal, engine  # ✅ Use session factory
from app.core.database.db_setup import init_superuser  # ✅ Import superuser setup
from app.core.config.settings import settings  # ✅ Import settings

# ✅ Configure Logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


def seed_data() -> None:
    """Seed the database with initial data."""
    try:
        with SessionLocal() as session:
            init_superuser(session)
            session.commit()
        logger.info("✅ Initial data successfully created!")
    except Exception as e:
        logger.error(f"❌ Database seeding failed: {e}", exc_info=True)
        sys.exit(1)


def main() -> None:
    """Main function to seed database."""

    # ✅ Prevent execution in production unless explicitly allowed
    if settings.ENVIRONMENT == "production":
        logger.warning("⚠️  Seeding data in production is disabled for safety!")
        sys.exit(1)

    logger.info("🌱 Seeding initial data...")
    seed_data()


if __name__ == "__main__":
    main()
