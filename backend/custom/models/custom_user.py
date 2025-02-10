from sqlmodel import SQLModel, Field
import uuid

class CustomUser(SQLModel, table=True):
    """
    A sample custom user model stored in the database.
    This will be auto-detected in migrations.
    """
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, index=True)
    name: str = Field(max_length=255, index=True)
    email: str = Field(unique=True, index=True, nullable=False)
    is_active: bool = Field(default=True)

