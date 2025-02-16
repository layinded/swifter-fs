from starlette.middleware.sessions import SessionMiddleware
from app.core.config.settings import settings

def setup_session(app):
    """Configure SessionMiddleware for the application."""
    app.add_middleware(
        SessionMiddleware,
        secret_key=settings.SECRET_KEY,  # Ensure this is a strong key
        max_age=86400,  # 1 day
        same_site="lax",
        https_only=False,
    )
