import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.routing import APIRoute

from app.api.main import api_router
from app.core.background_tasks import start_cache_refresh
from app.core.config.settings import settings
from app.core.database.db_setup import setup_database
from app.core.middleware.cors import setup_cors
from app.core.middleware.language import setup_language_middleware
from app.core.middleware.sentry import setup_sentry
from app.core.middleware.session import setup_session

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def custom_generate_unique_id(route: APIRoute) -> str:
    return f"{route.tags[0]}-{route.name}"


@asynccontextmanager
async def lifespan(app: FastAPI):  # noqa

    # Startup: Initialize the database
    logger.info("Running database initialization...")
    setup_database()
    logger.info("Database initialization complete.")

    # Startup: Start background tasks (e.g. cache refresh)
    logger.info("Starting cache refresh background task.")
    start_cache_refresh()

    # Yield control to the application (it will run until shutdown)
    yield

    # Shutdown logic here (if needed)
    logger.info("Shutting down application...")


# Create the app using the lifespan context manager
app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    generate_unique_id_function=custom_generate_unique_id,
    lifespan=lifespan,
)

# Setup middleware
setup_session(app)
logger.info("Session middleware set up.")

setup_sentry()
logger.info("Sentry middleware set up.")

setup_cors(app)
logger.info("CORS middleware set up.")

setup_language_middleware(app)
logger.info("Language middleware set up.")

# Include API routes
app.include_router(api_router, prefix=settings.API_V1_STR)
logger.info("API routes included. Application is ready to accept requests.")
