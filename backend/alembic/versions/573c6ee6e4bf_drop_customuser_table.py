"""Drop customuser table

Revision ID: 573c6ee6e4bf
Revises: 194f0a5dec70
Create Date: 2025-02-10 21:32:02.306316

"""
from alembic import op
import sqlalchemy as sa

# ✅ Revision identifiers, used by Alembic.
revision = '573c6ee6e4bf'
down_revision = '194f0a5dec70'
branch_labels = None
depends_on = None


def upgrade():
    """Drop the customuser table if it exists."""
    op.execute("DROP TABLE IF EXISTS customuser CASCADE;")  # ✅ Ensure table is dropped


def downgrade():
    """Recreate the customuser table only if it does not exist."""
    op.execute("""
        CREATE TABLE IF NOT EXISTS customuser (
            id UUID PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            email VARCHAR NOT NULL,
            is_active BOOLEAN NOT NULL
        );
    """)  # ✅ Ensures no duplicate table error
