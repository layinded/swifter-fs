import importlib
import os
import pkgutil
import sys
import warnings
from pathlib import Path

from sqlmodel import SQLModel

from app.models.common import Message

sys.path.append(str(Path(__file__).parent))

from app.core.utils.loader import dynamic_import

models_path = os.path.dirname(__file__)


__all__ = [name for _, name, _ in pkgutil.iter_modules([models_path])]

for module_name in __all__:
    try:
        importlib.import_module(f"app.models.{module_name}")
    except Exception as e:
        warnings.warn(f"Could not load core model `{module_name}`: {e}", stacklevel=2)


custom_models = dynamic_import("custom/models", "custom.models")

for model_name, module in custom_models.items():
    try:
        globals()[model_name] = module
    except Exception as e:
        warnings.warn(f"Could not load custom model `{model_name}`: {e}", stacklevel=2)


__all__.extend(["SQLModel", "Message"])
globals()["SQLModel"] = SQLModel
globals()["Message"] = Message
