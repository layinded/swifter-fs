import logging
from fastapi import FastAPI
from fastapi.routing import APIRoute
from app.api.main import api_router
from app.core.config.settings import settings
from app.core.database.db_setup import setup_database  # ✅ Import DB initializer
from app.core.middleware.cors import setup_cors  # ✅ Import CORS setup
from app.core.middleware.sentry import setup_sentry  # ✅ Import Sentry setup
from app.core.middleware.session import setup_session  # ✅ Import Session setup

# ✅ Configure Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def custom_generate_unique_id(route: APIRoute) -> str:
    """Generate a unique ID for each API route."""
    return f"{route.tags[0]}-{route.name}"


# ✅ Initialize FastAPI App
app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    generate_unique_id_function=custom_generate_unique_id,
)

# ✅ Set up session before anything else (fixes OAuth CSRF issues)
setup_session(app)

# ✅ Set up external dependencies
setup_sentry()
setup_cors(app)


# ✅ Run database initialization before starting
@app.on_event("startup")
async def startup_event():
    logger.info("🔄 Running database initialization...")
    setup_database()
    logger.info("✅ Database initialization complete.")


# ✅ Include API Routes (after setting up session)
app.include_router(api_router, prefix=settings.API_V1_STR)
