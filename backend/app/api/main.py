import warnings

from app.api.routes import auth_routes, oauth_routes, admin_routes
from app.api.routes import user_routes, utils_routes
from fastapi import APIRouter

# ✅ Initialize API Router
api_router = APIRouter()


def load_custom_routes(api_router: APIRouter):
    """
    Dynamically load all custom API modules in `custom.api`.
    """
    try:
        from custom.api import custom_api_router
        api_router.include_router(custom_api_router, prefix="/custom", tags=["Custom Modules"])
    except ImportError as e:
        warnings.warn(f"⚠️ Custom API modules could not be loaded: {str(e)}")


# ✅ Core API Routes
routes = [
    (auth_routes.router, "/auth", "Authentication"),
    (oauth_routes.router, "/oauth", "OAuth Logins"),
    (user_routes.router, "/users", "Users"),
    (admin_routes.router, "/admin", "Admin"),
    (utils_routes.router, "/utils", "Utilities"),
]

# ✅ Dynamically include all core routes
for router, prefix, tag in routes:
    api_router.include_router(router, prefix=prefix, tags=[tag])

# ✅ Load Custom and Private Routes
load_custom_routes(api_router)
