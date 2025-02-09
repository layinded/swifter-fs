from starlette.middleware.cors import CORSMiddleware
from app.core.config.settings import settings

def setup_cors(app):
    """Configure CORS for the application."""
    if settings.all_cors_origins:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=settings.all_cors_origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
