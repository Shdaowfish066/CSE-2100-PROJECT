"""add created_at to all models

Revision ID: b2c3d4e5f6a7
Revises: a1b2c3d4e5f6
Create Date: 2025-01-01 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


revision = 'b2c3d4e5f6a7'
down_revision = 'a1b2c3d4e5f6'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('created_at', sa.DateTime(), nullable=True, server_default=sa.text('now()')))
    op.execute("UPDATE posts SET created_at = now() WHERE created_at IS NULL")
    op.alter_column('posts', 'created_at', nullable=False)

    op.add_column('comments', sa.Column('created_at', sa.DateTime(), nullable=True, server_default=sa.text('now()')))
    op.execute("UPDATE comments SET created_at = now() WHERE created_at IS NULL")
    op.alter_column('comments', 'created_at', nullable=False)

    op.add_column('users', sa.Column('created_at', sa.DateTime(), nullable=True, server_default=sa.text('now()')))
    op.execute("UPDATE users SET created_at = now() WHERE created_at IS NULL")
    op.alter_column('users', 'created_at', nullable=False)

    op.add_column('votes', sa.Column('created_at', sa.DateTime(), nullable=True, server_default=sa.text('now()')))
    op.execute("UPDATE votes SET created_at = now() WHERE created_at IS NULL")
    op.alter_column('votes', 'created_at', nullable=False)

    op.add_column('files', sa.Column('created_at', sa.DateTime(), nullable=True, server_default=sa.text('now()')))
    op.execute("UPDATE files SET created_at = now() WHERE created_at IS NULL")
    op.alter_column('files', 'created_at', nullable=False)

    op.add_column('communities', sa.Column('created_at', sa.DateTime(), nullable=True, server_default=sa.text('now()')))
    op.execute("UPDATE communities SET created_at = now() WHERE created_at IS NULL")
    op.alter_column('communities', 'created_at', nullable=False)

    op.add_column('community_members', sa.Column('joined_at', sa.DateTime(), nullable=True, server_default=sa.text('now()')))
    op.execute("UPDATE community_members SET joined_at = now() WHERE joined_at IS NULL")
    op.alter_column('community_members', 'joined_at', nullable=False)

    op.add_column('community_posts', sa.Column('created_at', sa.DateTime(), nullable=True, server_default=sa.text('now()')))
    op.execute("UPDATE community_posts SET created_at = now() WHERE created_at IS NULL")
    op.alter_column('community_posts', 'created_at', nullable=False)


def downgrade() -> None:
    op.drop_column('community_posts', 'created_at')
    op.drop_column('community_members', 'joined_at')
    op.drop_column('communities', 'created_at')
    op.drop_column('files', 'created_at')
    op.drop_column('votes', 'created_at')
    op.drop_column('users', 'created_at')
    op.drop_column('comments', 'created_at')
    op.drop_column('posts', 'created_at')
