"""Add email verification and password reset fields

Revision ID: c6a1f8d7b2a1
Revises: ab3d9f3a8d21
Create Date: 2026-02-01

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c6a1f8d7b2a1'
down_revision = 'ab3d9f3a8d21'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('users', sa.Column('is_email_verified', sa.Boolean(), nullable=False, server_default=sa.text('false')))
    op.add_column('users', sa.Column('email_verification_token', sa.String(255), nullable=True))
    op.add_column('users', sa.Column('email_verification_expires', sa.DateTime(timezone=True), nullable=True))
    op.add_column('users', sa.Column('password_reset_token', sa.String(255), nullable=True))
    op.add_column('users', sa.Column('password_reset_expires', sa.DateTime(timezone=True), nullable=True))

    op.alter_column('users', 'is_email_verified', server_default=None)


def downgrade():
    op.drop_column('users', 'password_reset_expires')
    op.drop_column('users', 'password_reset_token')
    op.drop_column('users', 'email_verification_expires')
    op.drop_column('users', 'email_verification_token')
    op.drop_column('users', 'is_email_verified')
