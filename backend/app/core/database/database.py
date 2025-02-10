from sqlmodel import create_engine, Session
from sqlalchemy.orm import sessionmaker  # ✅ Use sessionmaker from SQLAlchemy

from app.core.config.settings import settings

# ✅ Singleton Database Engine
engine = create_engine(
    str(settings.SQLALCHEMY_DATABASE_URI),
    echo=False,  # ✅ Disable query logging in production
    pool_size=20,  # ✅ Max connections in pool
    max_overflow=10,  # ✅ Temporary overflow limit
)

# ✅ Create a session factory
SessionLocal = sessionmaker(bind=engine, class_=Session, expire_on_commit=False)


def get_session() -> Session:
    """Yields a new database session."""
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
