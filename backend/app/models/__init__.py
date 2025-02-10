import importlib
import warnings
import pkgutil
import sys
import os
from pathlib import Path
from sqlmodel import SQLModel
from app.models.common import Message  # ✅ Explicitly import Message

# ✅ Ensure `models/` directory is in the Python path
sys.path.append(str(Path(__file__).parent))

from app.core.utils.loader import dynamic_import

# ✅ Get the absolute path of `models/`
models_path = os.path.dirname(__file__)

# ✅ Import all built-in models in `models/`
__all__ = [name for _, name, _ in pkgutil.iter_modules([models_path])]

for module_name in __all__:
    try:
        importlib.import_module(f"app.models.{module_name}")
    except Exception as e:
        warnings.warn(f"⚠️ Could not load core model `{module_name}`: {e}")

# ✅ Dynamically load models from `CUSTOM/models`
custom_models = dynamic_import("custom/models", "custom.models")

for model_name, module in custom_models.items():
    try:
        globals()[model_name] = module
    except Exception as e:
        warnings.warn(f"⚠️ Could not load custom model `{model_name}`: {e}")

# ✅ Ensure SQLModel and Message are explicitly available
__all__.extend(["SQLModel", "Message"])
globals()["SQLModel"] = SQLModel  # ✅ Expose SQLModel for Alembic
globals()["Message"] = Message  # ✅ Expose Message model for imports
