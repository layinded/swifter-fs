from sqlalchemy.orm import sessionmaker
from sqlmodel import Session, create_engine

from app.core.config.settings import settings

engine = create_engine(
    str(settings.SQLALCHEMY_DATABASE_URI),
    echo=False,
    pool_size=20,
    max_overflow=10,
)


SessionLocal = sessionmaker(bind=engine, class_=Session, expire_on_commit=False)


def get_session() -> Session:
    """Yields a new database session."""
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
