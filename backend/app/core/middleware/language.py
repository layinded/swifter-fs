import logging

import jwt
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

from app.core.config.settings import settings
from app.core.database.database import SessionLocal
from app.core.security.refresh_token_service import ALGORITHM
from app.core.utils.cache_utils import load_translations_from_cache
from app.crud import crud_user

logger = logging.getLogger(__name__)


def setup_language_middleware(app):
    class LanguageMiddleware(BaseHTTPMiddleware):
        async def dispatch(self, request: Request, call_next):
            user_language = "en"

            try:
                auth_header = request.headers.get("authorization")
                logger.info(f"LanguageMiddleware: Received Auth Header: {auth_header}")

                if auth_header and auth_header.startswith("Bearer "):
                    token = auth_header.split(" ")[1]

                    # Decode token
                    payload = jwt.decode(
                        token, settings.SECRET_KEY, algorithms=[ALGORITHM]
                    )
                    user_email = payload.get("sub")  # Extract email
                    logger.info(
                        f"LanguageMiddleware: Decoded User Email from Token: {user_email}"
                    )

                    if user_email:
                        # Manually create a database session
                        session = SessionLocal()
                        try:
                            user = crud_user.get_user_by_email(
                                session=session, email=user_email
                            )
                            if user:
                                logger.info(
                                    f"LanguageMiddleware: Retrieved User - {user.email} | Preferred Language: {user.preferred_language}"
                                )
                                user_language = user.preferred_language
                            else:
                                logger.warning(
                                    f"LanguageMiddleware: No user found with email {user_email}"
                                )
                        finally:
                            session.close()  # Ensure session is closed

                # Fallback if no user found
                if user_language == "en":
                    headers = dict(request.headers)
                    user_language = (
                        headers.get("accept-language", "en").split(",")[0].strip()
                    )
                    logger.info(
                        f"LanguageMiddleware: No user language set, falling back to '{user_language}' from headers"
                    )

            except Exception as e:
                logger.error(
                    f"LanguageMiddleware: Error retrieving user language - {str(e)}"
                )

            # Load translations from cache
            translations = load_translations_from_cache().get(user_language, {})
            logger.info(
                f"LanguageMiddleware: Loaded {len(translations)} translations for '{user_language}'"
            )

            request.state.translations = translations
            response = await call_next(request)
            return response

    app.add_middleware(LanguageMiddleware)
