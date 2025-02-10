import importlib
import os
import sys
import warnings
from logging.config import fileConfig

from alembic import context

# ✅ Ensure the app directory is in Python's path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))

from app.core.database.database import engine  # ✅ Use Swifter-FS database

# ✅ Alembic Config object
config = context.config
fileConfig(config.config_file_name)

# ✅ Import core models
from app.models import SQLModel
from app.core.utils.loader import dynamic_import  # ✅ Import dynamic loader for custom models

# ✅ Dynamically load all models from CUSTOM/models
custom_models = dynamic_import("custom/models", "custom.models")

# ✅ Import custom models to ensure they are recognized by Alembic
for model_name, module in custom_models.items():
    try:
        importlib.import_module(f"custom.models.{model_name}")
    except Exception as e:
        warnings.warn(f"⚠️ Could not load custom model `{model_name}`: {e}")

# ✅ Target metadata for migrations
target_metadata = SQLModel.metadata

def run_migrations_offline():
    """Run migrations in 'offline' mode.'"""
    context.configure(
        url=str(engine.url),
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    """Run migrations in 'online' mode.'"""
    connectable = engine
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
