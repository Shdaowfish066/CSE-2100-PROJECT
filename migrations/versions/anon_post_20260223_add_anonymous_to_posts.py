"""Alembic migration to add is_anonymous and display_name columns to posts table."""

from alembic import op
import sqlalchemy as sa

revision = 'anon_post_20260223'
down_revision = '5c9ce2cd8641'
branch_labels = None
depends_on = None

def upgrade():
    op.add_column('posts', sa.Column('is_anonymous', sa.Boolean(), nullable=False, server_default=sa.text('false')))
    op.add_column('posts', sa.Column('display_name', sa.String(255), nullable=False, server_default=sa.text("''")))
    op.alter_column('posts', 'is_anonymous', server_default=None)
    op.alter_column('posts', 'display_name', server_default=None)

def downgrade():
    op.drop_column('posts', 'display_name')
    op.drop_column('posts', 'is_anonymous')
