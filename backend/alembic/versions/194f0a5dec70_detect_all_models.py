"""Detect all models

Revision ID: 194f0a5dec70
Revises: 654d23b7fb95
Create Date: 2025-02-10 19:39:24.595532

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel.sql.sqltypes
from sqlalchemy.dialects import postgresql

# ✅ Ensure dynamically loaded custom models are included
import importlib
import warnings
# from app.core.utils.loader import dynamic_import
import sys
import os

# ✅ Add backend root to Python path before imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from app.core.utils.loader import dynamic_import  # ✅ Import correctly without `app.`

# ✅ Load custom models dynamically
custom_models = dynamic_import("custom/models", "custom.models")

# ✅ Import all custom models to ensure they are part of the migration
for model_name, module in custom_models.items():
    try:
        importlib.import_module(f"custom.models.{model_name}")
    except Exception as e:
        warnings.warn(f"⚠️ Could not load custom model `{model_name}`: {e}")

# ✅ Revision identifiers, used by Alembic.
revision = '194f0a5dec70'
down_revision = '654d23b7fb95'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('customuser',
                    sa.Column('id', sa.Uuid(), nullable=False),
                    sa.Column('name', sqlmodel.sql.sqltypes.AutoString(length=255), nullable=False),
                    sa.Column('email', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
                    sa.Column('is_active', sa.Boolean(), nullable=False),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_index(op.f('ix_customuser_email'), 'customuser', ['email'], unique=True)
    op.create_index(op.f('ix_customuser_id'), 'customuser', ['id'], unique=False)
    op.create_index(op.f('ix_customuser_name'), 'customuser', ['name'], unique=False)
    op.alter_column('refreshtoken', 'expires_at',
                    existing_type=postgresql.TIMESTAMP(timezone=True),
                    type_=sa.DateTime(),
                    existing_nullable=False)
    op.alter_column('refreshtoken', 'created_at',
                    existing_type=postgresql.TIMESTAMP(timezone=True),
                    type_=sa.DateTime(),
                    existing_nullable=False,
                    existing_server_default=sa.text('now()'))
    op.drop_constraint('refreshtoken_token_key', 'refreshtoken', type_='unique')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint('refreshtoken_token_key', 'refreshtoken', ['token'])
    op.alter_column('refreshtoken', 'created_at',
                    existing_type=sa.DateTime(),
                    type_=postgresql.TIMESTAMP(timezone=True),
                    existing_nullable=False,
                    existing_server_default=sa.text('now()'))
    op.alter_column('refreshtoken', 'expires_at',
                    existing_type=sa.DateTime(),
                    type_=postgresql.TIMESTAMP(timezone=True),
                    existing_nullable=False)
    op.drop_index(op.f('ix_customuser_name'), table_name='customuser')
    op.drop_index(op.f('ix_customuser_id'), table_name='customuser')
    op.drop_index(op.f('ix_customuser_email'), table_name='customuser')
    op.drop_table('customuser')
    # ### end Alembic commands ###
