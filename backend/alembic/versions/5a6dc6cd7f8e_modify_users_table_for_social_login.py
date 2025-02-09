"""Modify user table for social login

Revision ID: 5a6dc6cd7f8e
Revises: a932af467a8a
Create Date: 2025-02-07 21:11:27.734664

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel.sql.sqltypes

# revision identifiers, used by Alembic.
revision = '5a6dc6cd7f8e'
down_revision = 'a932af467a8a'
branch_labels = None
depends_on = None


def upgrade():
    # Add new columns for social login
    op.add_column("user", sa.Column("auth_provider", sa.String(length=50), nullable=False, server_default="local"))
    op.add_column("user", sa.Column("provider_id", sa.String(length=255), unique=True, nullable=True))
    op.add_column("user", sa.Column("avatar_url", sa.Text(), nullable=True))

    # Make hashed_password nullable (for social logins)
    op.alter_column("user", "hashed_password", existing_type=sa.String(length=255), nullable=True)


def downgrade():
    # Reverse changes (if needed)
    op.drop_column("user", "auth_provider")
    op.drop_column("user", "provider_id")
    op.drop_column("user", "avatar_url")
    op.alter_column("user", "hashed_password", existing_type=sa.String(length=255), nullable=False)
