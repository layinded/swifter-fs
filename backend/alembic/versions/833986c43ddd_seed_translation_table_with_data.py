"""Seed translation table with data

Revision ID: 833986c43ddd
Revises: 7649cc2cc281
Create Date: 2025-02-26 11:17:08.716750

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel.sql.sqltypes
import importlib
import warnings
from app.core.utils.loader import dynamic_import

custom_models = dynamic_import("custom/models", "custom.models")

for model_name, module in custom_models.items():
    try:
        importlib.import_module(f"custom.models.{model_name}")
    except Exception as e:
        warnings.warn(f"Could not load custom model `{model_name}`: {e}")

revision = '833986c43ddd'
down_revision = '7649cc2cc281'
branch_labels = None
depends_on = None


def upgrade():
    # Clear the table if needed
    op.execute("TRUNCATE TABLE translation RESTART IDENTITY CASCADE;")

    # Now read and execute your SQL file
    import os
    current_dir = os.path.dirname(os.path.realpath(__file__))
    sql_file_path = os.path.join(current_dir, 'translation_data.sql')
    with open(sql_file_path, 'r', encoding='utf-8') as sql_file:
        sql_commands = sql_file.read()
    op.execute(sql_commands)


def downgrade():
    # Depending on your use case, you might reverse the seed data.
    # For example, if your SQL file inserted rows with a known key,
    # you could remove them here. Otherwise, you might leave this as a no-op.
    # Clear the table if needed
    op.execute("TRUNCATE TABLE translation RESTART IDENTITY CASCADE;")
