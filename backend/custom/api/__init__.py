from fastapi import APIRouter
import importlib
import pkgutil

custom_api_router = APIRouter()

# ✅ Automatically Import All API Modules in `custom.api`
package = __name__  # "custom.api"
for _, module_name, _ in pkgutil.iter_modules(__path__):
    module = importlib.import_module(f"{package}.{module_name}")
    if hasattr(module, "router"):
        custom_api_router.include_router(module.router, prefix=f"/{module_name}", tags=[module_name.capitalize()])
