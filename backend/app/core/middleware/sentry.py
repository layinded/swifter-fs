import sentry_sdk
from app.core.config.settings import settings

def setup_sentry():
    """Initialize Sentry for production environments."""
    if settings.SENTRY_DSN and settings.ENVIRONMENT != "local":
        sentry_sdk.init(dsn=str(settings.SENTRY_DSN), enable_tracing=True)
