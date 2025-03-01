import warnings

from fastapi import APIRouter, Depends

from app.api.routes import (
    admin_routes,
    auth_routes,
    oauth_routes,
    translation_routes,
    user_routes,
    utils_routes,
)
from app.core.security.dependencies import CurrentUser
from app.core.utils.loader import dynamic_import

api_router = APIRouter()

# Core API Routes
routes = [
    (auth_routes.router, "/auth", "Authentication"),
    (oauth_routes.router, "/oauth", "OAuth Logins"),
    (user_routes.router, "/users", "Users"),
    (admin_routes.router, "/admin", "Admin"),
    (utils_routes.router, "/utils", "Utilities"),
    (translation_routes.router, "/lang", "Languages"),
]

# Dynamically include all core routes
for router, prefix, tag in routes:
    api_router.include_router(router, prefix=prefix, tags=[tag])


def load_custom_routes(api_router: APIRouter):
    """
    Dynamically loads all custom API modules from `CUSTOM/api/` directory.
    - Routes with "private_" in their filename will require authentication.
    - Routes are tagged as "Custom Modules" in Swagger.
    """
    custom_routes_dict = dynamic_import("custom/api", "custom.api")

    if not custom_routes_dict:
        warnings.warn("No custom API routes found in `CUSTOM/api/`", stacklevel=2)

    for module_name, module in custom_routes_dict.items():
        is_protected = module_name.startswith("private_")

        if hasattr(module, "router"):
            if is_protected:
                print(f"Protecting route: {module_name}")
                module.router.dependencies.append(Depends(CurrentUser))

            api_router.include_router(module.router, tags=["Custom Modules"])
            print(f"Loaded custom route: {module_name}")


# Load Custom and Private Routes
load_custom_routes(api_router)
