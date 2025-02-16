from starlette.middleware.cors import CORSMiddleware

from app.core.config.settings import settings


def setup_cors(app):
    """Configure CORS for the application."""
    allowed_origins = settings.all_cors_origins if settings.all_cors_origins else ["*"]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=allowed_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
