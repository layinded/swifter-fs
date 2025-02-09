from sqlmodel import create_engine, Session
from app.core.config.settings import settings

# ✅ Singleton Database Engine
engine = create_engine(
    str(settings.SQLALCHEMY_DATABASE_URI),
    echo=False,  # ✅ Disable query logging in production
    pool_size=20,  # ✅ Max number of connections in the pool
    max_overflow=10,  # ✅ Allow temporary connections beyond pool size
)


def get_session() -> Session:
    """Returns a new database session."""
    return Session(engine)
