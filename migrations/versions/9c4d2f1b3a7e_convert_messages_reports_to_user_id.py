"""Convert messages/reports username references to user_id.

Revision ID: 9c4d2f1b3a7e
Revises: c6a1f8d7b2a1
Create Date: 2026-02-01

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "9c4d2f1b3a7e"
down_revision = "c6a1f8d7b2a1"
branch_labels = None
depends_on = None


def upgrade():
    # Messages: sender/recipient username -> user_id
    op.drop_constraint("messages_sender_username_fkey", "messages", type_="foreignkey")
    op.drop_constraint("messages_recipient_username_fkey", "messages", type_="foreignkey")

    op.add_column("messages", sa.Column("sender_id", sa.Integer(), nullable=True))
    op.add_column("messages", sa.Column("recipient_id", sa.Integer(), nullable=True))

    op.execute(
        """
        UPDATE messages
        SET sender_id = (SELECT id FROM users WHERE users.username = messages.sender_username)
        WHERE sender_username IS NOT NULL
        """
    )
    op.execute(
        """
        UPDATE messages
        SET recipient_id = (SELECT id FROM users WHERE users.username = messages.recipient_username)
        WHERE recipient_username IS NOT NULL
        """
    )

    op.drop_index("ix_messages_sender_username", table_name="messages")
    op.drop_index("ix_messages_recipient_username", table_name="messages")
    op.drop_column("messages", "sender_username")
    op.drop_column("messages", "recipient_username")

    op.alter_column("messages", "sender_id", existing_type=sa.Integer(), nullable=False)
    op.alter_column("messages", "recipient_id", existing_type=sa.Integer(), nullable=False)

    op.create_foreign_key("messages_sender_id_fkey", "messages", "users", ["sender_id"], ["id"])
    op.create_foreign_key("messages_recipient_id_fkey", "messages", "users", ["recipient_id"], ["id"])
    op.create_index(op.f("ix_messages_sender_id"), "messages", ["sender_id"], unique=False)
    op.create_index(op.f("ix_messages_recipient_id"), "messages", ["recipient_id"], unique=False)

    op.alter_column(
        "messages",
        "is_read",
        existing_type=sa.Integer(),
        type_=sa.Boolean(),
        nullable=False,
        postgresql_using="is_read::boolean",
    )

    # Reports: reporter username -> user_id
    op.drop_constraint("reports_reporter_username_fkey", "reports", type_="foreignkey")
    op.add_column("reports", sa.Column("reporter_id", sa.Integer(), nullable=True))

    op.execute(
        """
        UPDATE reports
        SET reporter_id = (SELECT id FROM users WHERE users.username = reports.reporter_username)
        WHERE reporter_username IS NOT NULL
        """
    )

    op.drop_index("ix_reports_reporter_username", table_name="reports")
    op.drop_column("reports", "reporter_username")

    op.alter_column("reports", "reporter_id", existing_type=sa.Integer(), nullable=False)
    op.create_foreign_key("reports_reporter_id_fkey", "reports", "users", ["reporter_id"], ["id"])
    op.create_index(op.f("ix_reports_reporter_id"), "reports", ["reporter_id"], unique=False)


def downgrade():
    # Reports: user_id -> username
    op.drop_index(op.f("ix_reports_reporter_id"), table_name="reports")
    op.drop_constraint("reports_reporter_id_fkey", "reports", type_="foreignkey")
    op.add_column("reports", sa.Column("reporter_username", sa.String(255), nullable=True))

    op.execute(
        """
        UPDATE reports
        SET reporter_username = (SELECT username FROM users WHERE users.id = reports.reporter_id)
        WHERE reporter_id IS NOT NULL
        """
    )

    op.alter_column("reports", "reporter_username", existing_type=sa.String(255), nullable=False)
    op.create_foreign_key(
        "reports_reporter_username_fkey",
        "reports",
        "users",
        ["reporter_username"],
        ["username"],
    )
    op.create_index("ix_reports_reporter_username", "reports", ["reporter_username"], unique=False)
    op.drop_column("reports", "reporter_id")

    # Messages: user_id -> username
    op.drop_index(op.f("ix_messages_sender_id"), table_name="messages")
    op.drop_index(op.f("ix_messages_recipient_id"), table_name="messages")
    op.drop_constraint("messages_sender_id_fkey", "messages", type_="foreignkey")
    op.drop_constraint("messages_recipient_id_fkey", "messages", type_="foreignkey")
    op.add_column("messages", sa.Column("sender_username", sa.String(255), nullable=True))
    op.add_column("messages", sa.Column("recipient_username", sa.String(255), nullable=True))

    op.execute(
        """
        UPDATE messages
        SET sender_username = (SELECT username FROM users WHERE users.id = messages.sender_id)
        WHERE sender_id IS NOT NULL
        """
    )
    op.execute(
        """
        UPDATE messages
        SET recipient_username = (SELECT username FROM users WHERE users.id = messages.recipient_id)
        WHERE recipient_id IS NOT NULL
        """
    )

    op.alter_column("messages", "sender_username", existing_type=sa.String(255), nullable=False)
    op.alter_column("messages", "recipient_username", existing_type=sa.String(255), nullable=False)

    op.create_foreign_key(
        "messages_sender_username_fkey",
        "messages",
        "users",
        ["sender_username"],
        ["username"],
    )
    op.create_foreign_key(
        "messages_recipient_username_fkey",
        "messages",
        "users",
        ["recipient_username"],
        ["username"],
    )
    op.create_index("ix_messages_sender_username", "messages", ["sender_username"], unique=False)
    op.create_index("ix_messages_recipient_username", "messages", ["recipient_username"], unique=False)
    op.drop_column("messages", "sender_id")
    op.drop_column("messages", "recipient_id")

    op.alter_column(
        "messages",
        "is_read",
        existing_type=sa.Boolean(),
        type_=sa.Integer(),
        nullable=False,
        postgresql_using="is_read::int",
    )
