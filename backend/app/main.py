import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.routing import APIRoute

from app.api.main import api_router
from app.core.config.settings import settings
from app.core.database.db_setup import setup_database
from app.core.middleware.cors import setup_cors
from app.core.middleware.sentry import setup_sentry
from app.core.middleware.session import setup_session

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def custom_generate_unique_id(route: APIRoute) -> str:
    """Generate a unique ID for each API route."""
    return f"{route.tags[0]}-{route.name}"


@asynccontextmanager

async def lifespan(app: FastAPI):  # noqa: ARG001

    # Startup: Initialize the database
    logger.info("Running database initialization...")
    setup_database()
    logger.info("Database initialization complete.")

    # Yield control to the application (runs until shutdown)
    yield

    # Shutdown: (add any cleanup tasks here if needed)
    logger.info("Shutting down application...")


app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    generate_unique_id_function=custom_generate_unique_id,
    lifespan=lifespan,
)

setup_session(app)

setup_sentry()
setup_cors(app)

app.include_router(api_router, prefix=settings.API_V1_STR)
