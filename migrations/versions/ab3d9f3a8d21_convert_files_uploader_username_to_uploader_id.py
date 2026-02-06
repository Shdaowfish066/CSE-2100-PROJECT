"""Convert files.uploader_username to files.uploader_id

Revision ID: ab3d9f3a8d21
Revises: f2b7c1d9e0aa
Create Date: 2026-02-01

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ab3d9f3a8d21'
down_revision = 'f2b7c1d9e0aa'
branch_labels = None
depends_on = None


def upgrade():
    # Drop foreign key on uploader_username
    op.drop_constraint('files_uploader_username_fkey', 'files', type_='foreignkey')

    # Add new uploader_id column as nullable first
    op.add_column('files', sa.Column('uploader_id', sa.Integer(), nullable=True))

    # Populate uploader_id from uploader_username using users table
    op.execute('''
        UPDATE files
        SET uploader_id = (SELECT id FROM users WHERE users.username = files.uploader_username)
        WHERE uploader_username IS NOT NULL
    ''')

    # Drop old index and column
    op.drop_index('ix_files_uploader_username', table_name='files')
    op.drop_column('files', 'uploader_username')

    # Make uploader_id NOT NULL
    op.alter_column('files', 'uploader_id', existing_type=sa.Integer(), nullable=False)

    # Add new foreign key and index
    op.create_foreign_key('files_uploader_id_fkey', 'files', 'users', ['uploader_id'], ['id'])
    op.create_index(op.f('ix_files_uploader_id'), 'files', ['uploader_id'], unique=False)


def downgrade():
    # Restore uploader_username column
    op.add_column('files', sa.Column('uploader_username', sa.String(255), nullable=True))

    # Populate uploader_username from uploader_id
    op.execute('''
        UPDATE files
        SET uploader_username = (SELECT username FROM users WHERE users.id = files.uploader_id)
        WHERE uploader_id IS NOT NULL
    ''')

    # Make uploader_username NOT NULL and add foreign key + index
    op.alter_column('files', 'uploader_username', existing_type=sa.String(255), nullable=False)
    op.create_foreign_key('files_uploader_username_fkey', 'files', 'users', ['uploader_username'], ['username'])
    op.create_index('ix_files_uploader_username', 'files', ['uploader_username'], unique=False)

    # Drop uploader_id foreign key/index and column
    op.drop_index(op.f('ix_files_uploader_id'), table_name='files')
    op.drop_constraint('files_uploader_id_fkey', 'files', type_='foreignkey')
    op.drop_column('files', 'uploader_id')
