from fastapi import Request

from app.core.utils.cache_utils import load_translations_from_cache


def translate(request: Request, key: str, **kwargs) -> str:
    """
    Look up the translation for a given key from request.state.translations.
    If not found, fall back to the default language ('en') translations; otherwise, return the key.
    """
    # Try to get current translations from the request state
    translations = getattr(request.state, "translations", {})
    text = translations.get(key)

    if text is None:
        # Fallback: load default translations for 'en' from the cache
        all_translations = load_translations_from_cache()

        default_translations = all_translations.get("en", {})
        text = default_translations.get(key, key)

    return text.format(**kwargs) if kwargs else text
