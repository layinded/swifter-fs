import json
import logging
import os
import uuid

CACHE_FILE = "translation_cache.json"
logger = logging.getLogger(__name__)


def default_serializer(obj):
    if isinstance(obj, uuid.UUID):
        return str(obj)
    raise TypeError(f"Object of type {obj.__class__.__name__} is not JSON serializable")


def save_translations_to_cache(translations: dict):
    try:
        with open(CACHE_FILE, "w") as file:
            json.dump(translations, file, indent=4, default=default_serializer)
        logger.info("Successfully saved translations to cache file '%s'.", CACHE_FILE)
    except Exception as e:
        logger.error("Failed to save translations to cache: %s", e)


def load_translations_from_cache():
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE) as file:
                translations = json.load(file)
            logger.info(
                "Successfully loaded translations from cache file '%s'.", CACHE_FILE
            )
            return translations
        except Exception as e:
            logger.error("Failed to load translations from cache: %s", e)
            return {}
    logger.info(
        "Cache file '%s' does not exist; returning empty translations.", CACHE_FILE
    )
    return {}
