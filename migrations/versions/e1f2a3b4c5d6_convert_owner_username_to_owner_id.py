"""Convert owner_username to owner_id

Revision ID: e1f2a3b4c5d6
Revises: bc162c604430
Create Date: 2026-02-01

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e1f2a3b4c5d6'
down_revision = 'bc162c604430'
branch_labels = None
depends_on = None


def upgrade():
    # Drop foreign key constraints first
    op.drop_constraint('posts_owner_username_fkey', 'posts', type_='foreignkey')
    op.drop_constraint('comments_owner_username_fkey', 'comments', type_='foreignkey')
    
    # Add new owner_id columns as nullable first
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=True))
    op.add_column('comments', sa.Column('owner_id', sa.Integer(), nullable=True))
    
    # Populate owner_id from owner_username using a join with users table
    op.execute('''
        UPDATE posts 
        SET owner_id = (SELECT id FROM users WHERE users.username = posts.owner_username)
        WHERE owner_username IS NOT NULL
    ''')
    
    op.execute('''
        UPDATE comments 
        SET owner_id = (SELECT id FROM users WHERE users.username = comments.owner_username)
        WHERE owner_username IS NOT NULL
    ''')
    
    # Drop the old columns
    op.drop_column('posts', 'owner_username')
    op.drop_column('comments', 'owner_username')
    
    # Make owner_id NOT NULL
    op.alter_column('posts', 'owner_id', existing_type=sa.Integer(), nullable=False)
    op.alter_column('comments', 'owner_id', existing_type=sa.Integer(), nullable=False)
    
    # Add foreign keys and indexes
    op.create_foreign_key('posts_owner_id_fkey', 'posts', 'users', ['owner_id'], ['id'])
    op.create_foreign_key('comments_owner_id_fkey', 'comments', 'users', ['owner_id'], ['id'])
    
    op.create_index(op.f('ix_posts_owner_id'), 'posts', ['owner_id'], unique=False)
    op.create_index(op.f('ix_comments_owner_id'), 'comments', ['owner_id'], unique=False)


def downgrade():
    # Drop indexes
    op.drop_index(op.f('ix_posts_owner_id'), table_name='posts')
    op.drop_index(op.f('ix_comments_owner_id'), table_name='comments')
    
    # Drop foreign keys and new columns
    op.drop_constraint('posts_owner_id_fkey', 'posts', type_='foreignkey')
    op.drop_constraint('comments_owner_id_fkey', 'comments', type_='foreignkey')
    
    op.drop_column('posts', 'owner_id')
    op.drop_column('comments', 'owner_id')
    
    # Restore old columns
    op.add_column('posts', sa.Column('owner_username', sa.String(255), nullable=False))
    op.add_column('comments', sa.Column('owner_username', sa.String(255), nullable=False))
    
    op.create_foreign_key('posts_owner_username_fkey', 'posts', 'users', ['owner_username'], ['username'])
    op.create_foreign_key('comments_owner_username_fkey', 'comments', 'users', ['owner_username'], ['username'])
