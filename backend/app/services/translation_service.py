from app.core.database.dependencies import SessionDep
from app.core.utils.cache_utils import (
    load_translations_from_cache,
    save_translations_to_cache,
)
from app.crud import crud_translation
from app.models.translation import Translation


async def add_translation(db: SessionDep, language_code: str, key: str, value: str):
    new_translation = crud_translation.create_translation(
        db, Translation(language_code=language_code, key=key, value=value)
    )
    translations = load_translations_from_cache()
    translations.setdefault(language_code, {})[key] = value
    save_translations_to_cache(translations)
    return new_translation


def fetch_translations(db: SessionDep, language_code: str):
    return crud_translation.get_translations_by_language(db, language_code)


def fetch_translation(db: SessionDep, language_code: str, key: str):
    return crud_translation.get_translation_by_key(db, language_code, key)


async def modify_translation(
    db: SessionDep, translation_id: str, translation_data: dict
):
    updated_translation = crud_translation.update_translation(
        db, translation_id, translation_data
    )
    translations = load_translations_from_cache()
    translations[updated_translation.language_code][
        updated_translation.key
    ] = updated_translation.value
    save_translations_to_cache(translations)
    return updated_translation


async def remove_translation(db: SessionDep, translation_id: str):
    translation = crud_translation.delete_translation(db, translation_id)
    translations = load_translations_from_cache()
    if translation.language_code in translations:
        translations[translation.language_code].pop(translation.key, None)
    save_translations_to_cache(translations)
    return translation


async def fetch_all_translations_bulk(db: SessionDep, languages: list[str]) -> dict:
    """
    Fetch translations for multiple languages at once and return a dictionary
    mapping language codes to translation dictionaries.
    """
    translations_dict = {}
    for lang in languages:
        translations = crud_translation.get_translations_by_language(db, lang)
        # Build a dictionary: key is the translation key, value is its translation value
        translations_dict[lang] = {t.key: t.value for t in translations}
    return translations_dict
