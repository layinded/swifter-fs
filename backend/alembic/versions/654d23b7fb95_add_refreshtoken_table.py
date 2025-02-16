from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '654d23b7fb95'
down_revision = '2bd5358684d9'
branch_labels = None
depends_on = None


def upgrade():
    # ✅ Manually create the RefreshToken table
    op.create_table(
        'refreshtoken',
        sa.Column('id', sa.UUID(), primary_key=True, nullable=False),
        sa.Column('user_email', sa.String(255), nullable=False, index=True),
        sa.Column('token', sa.String(500), nullable=False, unique=True),
        sa.Column('expires_at', sa.TIMESTAMP(timezone=True), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.func.now(), nullable=False),
    )


def downgrade():
    # ✅ Drop the table if we need to rollback
    op.drop_table('refreshtoken')
