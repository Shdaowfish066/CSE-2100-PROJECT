"""add communities feature

Revision ID: a1b2c3d4e5f6
Revises: 4b16424da1b7
Create Date: 2026-02-24 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

revision = 'a1b2c3d4e5f6'
down_revision = '4b16424da1b7'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'communities',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('captain_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['captain_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(op.f('ix_communities_id'), 'communities', ['id'], unique=False)
    op.create_index(op.f('ix_communities_name'), 'communities', ['name'], unique=True)
    op.create_index(op.f('ix_communities_captain_id'), 'communities', ['captain_id'], unique=False)

    op.create_table(
        'community_members',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('community_id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('role', sa.Enum('captain', 'member', name='memberrole'), nullable=False),
        sa.ForeignKeyConstraint(['community_id'], ['communities.id'], ),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('community_id', 'user_id', name='uq_community_user'),
    )
    op.create_index(op.f('ix_community_members_id'), 'community_members', ['id'], unique=False)
    op.create_index(op.f('ix_community_members_community_id'), 'community_members', ['community_id'], unique=False)
    op.create_index(op.f('ix_community_members_user_id'), 'community_members', ['user_id'], unique=False)

    op.create_table(
        'community_posts',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('community_id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('owner_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['community_id'], ['communities.id'], ),
        sa.ForeignKeyConstraint(['owner_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(op.f('ix_community_posts_id'), 'community_posts', ['id'], unique=False)
    op.create_index(op.f('ix_community_posts_community_id'), 'community_posts', ['community_id'], unique=False)
    op.create_index(op.f('ix_community_posts_owner_id'), 'community_posts', ['owner_id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_community_posts_owner_id'), table_name='community_posts')
    op.drop_index(op.f('ix_community_posts_community_id'), table_name='community_posts')
    op.drop_index(op.f('ix_community_posts_id'), table_name='community_posts')
    op.drop_table('community_posts')

    op.drop_index(op.f('ix_community_members_user_id'), table_name='community_members')
    op.drop_index(op.f('ix_community_members_community_id'), table_name='community_members')
    op.drop_index(op.f('ix_community_members_id'), table_name='community_members')
    op.drop_table('community_members')
    op.execute("DROP TYPE IF EXISTS memberrole")

    op.drop_index(op.f('ix_communities_captain_id'), table_name='communities')
    op.drop_index(op.f('ix_communities_name'), table_name='communities')
    op.drop_index(op.f('ix_communities_id'), table_name='communities')
    op.drop_table('communities')
