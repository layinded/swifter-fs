import os
import sys
from logging.config import fileConfig

from alembic import context

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))

from app.core.database.database import engine

config = context.config
fileConfig(config.config_file_name)

from app.models import SQLModel
from app.core.utils.loader import dynamic_import

custom_models = dynamic_import("backend/custom/models", "custom.models")

for model_name, module in custom_models.items():
    try:
        importlib.import_module(f"custom.models.{model_name}")
    except Exception as e:
        warnings.warn(f"Could not load custom model `{model_name}`: {e}")

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
