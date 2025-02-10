from sqlmodel import Session
from fastapi import Depends
from collections.abc import Generator
from typing import Annotated
from app.core.database.database import SessionLocal

def get_db() -> Generator[Session, None, None]:
    """Yields a new database session."""
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()  # ✅ Ensure the session is properly closed

# ✅ Type Alias for Dependency Injection
SessionDep = Annotated[Session, Depends(get_db)]
