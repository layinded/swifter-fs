import asyncio
import logging

from app.core.database.database import SessionLocal  # Your session factory
from app.core.utils.cache_utils import save_translations_to_cache
from app.services.translation_service import fetch_all_translations_bulk

logger = logging.getLogger(__name__)


async def refresh_translation_cache():
    languages = ["en", "cs"]  # Add more languages if needed
    while True:
        logger.info("Refreshing translation cache for languages: %s", languages)
        try:
            # Create a new session explicitly from SessionLocal
            with SessionLocal() as db:
                # fetch_all_translations_bulk should return a list or a dict with all translations.
                translations = await fetch_all_translations_bulk(db, languages)
                if translations:
                    save_translations_to_cache(translations)
                    logger.info(
                        "Translation cache refreshed successfully. Cache file updated."
                    )
                else:
                    logger.warning("No translations were fetched from the database.")
        except Exception as e:
            logger.error("Error refreshing translation cache: %s", e)
        await asyncio.sleep(3600)  # Wait one hour before refreshing again


def start_cache_refresh():
    loop = asyncio.get_event_loop()
    loop.create_task(refresh_translation_cache())
    logger.info("Started translation cache refresh background task.")
