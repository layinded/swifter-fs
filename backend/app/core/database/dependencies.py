from sqlmodel import Session
from fastapi import Depends
from collections.abc import Generator
from typing import Annotated
from app.core.database.database import get_session

def get_db() -> Generator[Session, None, None]:
    """Yields a new database session."""
    with get_session() as session:
        yield session

# ✅ Type Alias for Dependency Injection
SessionDep = Annotated[Session, Depends(get_db)]
