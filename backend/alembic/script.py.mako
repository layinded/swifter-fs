"""${message}

Revision ID: ${up_revision}
Revises: ${down_revision | comma,n}
Create Date: ${create_date}

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel.sql.sqltypes
${imports if imports else ""}

import importlib
import warnings
from app.core.utils.loader import dynamic_import


custom_models = dynamic_import("custom/models", "custom.models")


for model_name, module in custom_models.items():
    try:
        importlib.import_module(f"custom.models.{model_name}")
    except Exception as e:
        warnings.warn(f"Could not load custom model `{model_name}`: {e}")


revision = ${repr(up_revision)}
down_revision = ${repr(down_revision)}
branch_labels = ${repr(branch_labels)}
depends_on = ${repr(depends_on)}

def upgrade():
    ${upgrades if upgrades else "pass"}

def downgrade():
    ${downgrades if downgrades else "pass"}
