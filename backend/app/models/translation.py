import uuid

from sqlmodel import Field, SQLModel


class TranslationBase(SQLModel):
    language_code: str = Field(max_length=5, index=True)  # e.g., 'en', 'cs'
    key: str = Field(max_length=255, index=True)  # e.g., 'welcome_message'
    value: str = Field(max_length=1000)  # Translated text


class Translation(TranslationBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)


class TranslationCreate(TranslationBase):
    pass


class TranslationUpdate(TranslationBase):
    language_code: str | None = None
    key: str | None = None
    value: str | None = None


class TranslationPublic(TranslationBase):
    id: uuid.UUID


class TranslationCreateSchema(TranslationBase):
    language_code: str = Field(
        ..., min_length=2, max_length=5, description="Language code (e.g., 'en', 'cs')"
    )
    key: str = Field(..., min_length=1, max_length=255, description="Translation key")
    value: str = Field(..., min_length=1, description="Translation value")
