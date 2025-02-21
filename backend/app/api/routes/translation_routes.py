import uuid
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Query, Request
from pydantic import BaseModel

from app.core.security.dependencies import SessionDep, get_current_active_superuser
from app.core.utils.translation_helper import translate
from app.models.translation import (
    TranslationCreate,
    TranslationCreateSchema,
    TranslationPublic,
    TranslationUpdate,
)
from app.services import translation_service

router = APIRouter()


# Composite response model for endpoints returning both a message and a translation
class TranslationResponse(BaseModel):
    message: str
    translation: TranslationPublic


@router.post(
    "/",
    dependencies=[Depends(get_current_active_superuser)],
    response_model=TranslationResponse,
    operation_id="create_translation",
)
async def create_translation_route(
    translation_in: TranslationCreate,
    db: SessionDep,
    request: Request = None,
) -> Any:
    """
    Create a new translation.
    """
    new_translation = await translation_service.add_translation(
        db, translation_in.language_code, translation_in.key, translation_in.value
    )
    return {
        "message": translate(request, "translation_created"),
        "translation": new_translation,
    }


@router.get(
    "/{language_code}",
    response_model=list[TranslationPublic],
    operation_id="get_translations",
)
async def get_translations_route(
    language_code: str,
    db: SessionDep,
    request: Request = None,
) -> Any:
    """
    Retrieve all translations for the specified language.
    """
    translations = translation_service.fetch_translations(db, language_code)
    if not translations:
        raise HTTPException(
            status_code=404, detail=translate(request, "no_translations_found")
        )
    return translations


@router.get(
    "/{language_code}/{key}",
    response_model=TranslationPublic,
    operation_id="get_translation",
)
async def get_translation_route(
    language_code: str,
    key: str,
    db: SessionDep,
    request: Request = None,
) -> Any:
    """
    Retrieve a specific translation by language code and key.
    """
    translation = translation_service.fetch_translation(db, language_code, key)
    if not translation:
        raise HTTPException(
            status_code=404, detail=translate(request, "no_translations_found")
        )
    return translation


@router.put(
    "/{translation_id}",
    dependencies=[Depends(get_current_active_superuser)],
    response_model=TranslationResponse,
    operation_id="update_translation",
)
async def update_translation_route(
    translation_id: uuid.UUID,
    translation_in: TranslationUpdate,
    db: SessionDep,
    request: Request = None,
) -> Any:
    """
    Update an existing translation.
    """
    updated_translation = await translation_service.modify_translation(
        db, translation_id, translation_in
    )
    return {
        "message": translate(request, "translation_updated"),
        "translation": updated_translation,
    }


@router.delete(
    "/{translation_id}",
    dependencies=[Depends(get_current_active_superuser)],
    operation_id="delete_translation",
)
async def delete_translation_route(
    translation_id: uuid.UUID,
    db: SessionDep,
    request: Request = None,
) -> Any:
    """
    Delete a translation by its ID.
    """
    await translation_service.remove_translation(db, translation_id)
    return {"message": translate(request, "translation_deleted")}


@router.get(
    "/translations/bulk/",
    dependencies=[Depends(get_current_active_superuser)],
    response_model=dict[str, dict[str, str]],
    # Return a dictionary mapping language codes to key-value translation dicts
    operation_id="get_bulk_translations",
)
async def get_bulk_translations_route(
    request: Request,
    db: SessionDep,
    languages: list[str] = Query(...),
) -> Any:
    """
    Retrieve translations in bulk for a list of languages.
    """
    translations = await translation_service.fetch_all_translations_bulk(db, languages)
    if not translations:
        raise HTTPException(
            status_code=404, detail=translate(request, "no_bulk_translations_found")
        )
    return translations


@router.post(
    "/bulk/",
    dependencies=[Depends(get_current_active_superuser)],
    response_model=dict,  # Returning a dict with a "message" key
    operation_id="bulk_insert_translations",
)
async def bulk_insert_translations_route(
    translations: list[TranslationCreateSchema],  # Use validated schema
    db: SessionDep,
    request: Request = None,
) -> Any:
    """
    Bulk insert translations and return a success or failure message.
    """
    inserted_count = 0
    failed_keys = []

    for translation in translations:
        try:
            await translation_service.add_translation(
                db, translation.language_code, translation.key, translation.value
            )
            inserted_count += 1
        except Exception:
            failed_keys.append(translation.key)

    # Commit changes after processing all translations
    db.commit()

    if inserted_count == len(translations):
        message = translate(request, "new_translation_created")
    else:
        message = translate(
            request, "translation_creation_failed", keys=", ".join(failed_keys)
        )

    return {"message": message}
