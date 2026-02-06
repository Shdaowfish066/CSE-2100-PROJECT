"""Convert votes.username to votes.user_id

Revision ID: f2b7c1d9e0aa
Revises: e1f2a3b4c5d6
Create Date: 2026-02-01

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f2b7c1d9e0aa'
down_revision = 'e1f2a3b4c5d6'
branch_labels = None
depends_on = None


def upgrade():
    # Drop foreign key on username
    op.drop_constraint('votes_username_fkey', 'votes', type_='foreignkey')

    # Add new user_id column as nullable first
    op.add_column('votes', sa.Column('user_id', sa.Integer(), nullable=True))

    # Populate user_id from username using users table
    op.execute('''
        UPDATE votes
        SET user_id = (SELECT id FROM users WHERE users.username = votes.username)
        WHERE username IS NOT NULL
    ''')

    # Drop old index and column
    op.drop_index('ix_votes_username', table_name='votes')
    op.drop_column('votes', 'username')

    # Make user_id NOT NULL
    op.alter_column('votes', 'user_id', existing_type=sa.Integer(), nullable=False)

    # Add new foreign key and index
    op.create_foreign_key('votes_user_id_fkey', 'votes', 'users', ['user_id'], ['id'])
    op.create_index(op.f('ix_votes_user_id'), 'votes', ['user_id'], unique=False)


def downgrade():
    # Restore username column
    op.add_column('votes', sa.Column('username', sa.String(255), nullable=True))

    # Populate username from user_id
    op.execute('''
        UPDATE votes
        SET username = (SELECT username FROM users WHERE users.id = votes.user_id)
        WHERE user_id IS NOT NULL
    ''')

    # Make username NOT NULL and add foreign key + index
    op.alter_column('votes', 'username', existing_type=sa.String(255), nullable=False)
    op.create_foreign_key('votes_username_fkey', 'votes', 'users', ['username'], ['username'])
    op.create_index('ix_votes_username', 'votes', ['username'], unique=False)

    # Drop user_id foreign key/index and column
    op.drop_index(op.f('ix_votes_user_id'), table_name='votes')
    op.drop_constraint('votes_user_id_fkey', 'votes', type_='foreignkey')
    op.drop_column('votes', 'user_id')
