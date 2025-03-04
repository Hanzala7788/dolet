"""fix User table name

Revision ID: 3000a6e48a83
Revises: b5cbe0662017
Create Date: 2025-02-27 07:31:36.631439

"""

from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from sqlalchemy import text  # Import text for executing raw SQL

# revision identifiers, used by Alembic.
revision: str = "3000a6e48a83"
down_revision: Union[str, None] = "b5cbe0662017"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    conn = op.get_bind()

    # Drop the old indexes if they exist
    existing_indexes = conn.execute(
        text("SELECT * FROM pg_indexes WHERE indexname = 'idx_email_active'")
    ).fetchall()
    if existing_indexes:
        op.drop_index("idx_email_active", table_name="users")

    existing_indexes = conn.execute(
        text("SELECT * FROM pg_indexes WHERE indexname = 'ix_users_Email'")
    ).fetchall()
    if existing_indexes:
        op.drop_index("ix_users_Email", table_name="users")

    existing_indexes = conn.execute(
        text("SELECT * FROM pg_indexes WHERE indexname = 'ix_users_UserId'")
    ).fetchall()
    if existing_indexes:
        op.drop_index("ix_users_UserId", table_name="users")

    # Check if the old table exists
    table_exists = (
        conn.execute(text("SELECT to_regclass('public.users')")).scalar() is not None
    )
    if table_exists:
        op.drop_table("users")

    # Create the new User table
    op.create_table(
        "User",
        sa.Column("UserId", sa.UUID(), nullable=False),
        sa.Column("Email", sa.String(), nullable=True),
        sa.Column("HashedPassword", sa.String(), nullable=True),
        sa.Column("IsActive", sa.Boolean(), nullable=True),
        sa.Column("IsArchived", sa.Boolean(), nullable=True),
        sa.Column("ArchivedAt", sa.DateTime(timezone=True), nullable=True),
        sa.Column("CreatedAt", sa.DateTime(timezone=True), nullable=True),
        sa.Column("UpdatedAt", sa.DateTime(timezone=True), nullable=True),
        sa.Column("ArchivedBy", sa.String(length=100), nullable=True),
        sa.Column("CreatedBy", sa.String(length=100), nullable=True),
        sa.Column("UpdatedBy", sa.String(length=100), nullable=True),
        sa.PrimaryKeyConstraint("UserId"),
    )

    # Create new indexes
    op.create_index("idx_email_active", "User", ["Email", "IsActive"], unique=False)
    op.create_index(op.f("ix_User_Email"), "User", ["Email"], unique=True)
    op.create_index(op.f("ix_User_UserId"), "User", ["UserId"], unique=False)


def downgrade() -> None:
    # Drop the new indexes and table
    op.drop_index(op.f("ix_User_UserId"), table_name="User ")
    op.drop_index(op.f("ix_User_Email"), table_name="User ")
    op.drop_index("idx_email_active", table_name="User ")
    op.drop_table("User ")

    # Recreate the old users table
    op.create_table(
        "users",
        sa.Column("Email", sa.VARCHAR(), autoincrement=False, nullable=True),
        sa.Column("HashedPassword", sa.VARCHAR(), autoincrement=False, nullable=True),
        sa.Column("IsActive", sa.BOOLEAN(), autoincrement=False, nullable=True),
        sa.Column("IsArchived", sa.BOOLEAN(), autoincrement=False, nullable=True),
        sa.Column(
            "ArchivedAt",
            postgresql.TIMESTAMP(timezone=True),
            autoincrement=False,
            nullable=True,
        ),
        sa.Column(
            "CreatedAt",
            postgresql.TIMESTAMP(timezone=True),
            autoincrement=False,
            nullable=True,
        ),
        sa.Column(
            "UpdatedAt",
            postgresql.TIMESTAMP(timezone=True),
            autoincrement=False,
            nullable=True,
        ),
        sa.Column(
            "ArchivedBy", sa.VARCHAR(length=100), autoincrement=False, nullable=True
        ),
        sa.Column(
            "CreatedBy", sa.VARCHAR(length=100), autoincrement=False, nullable=True
        ),
        sa.Column(
            "UpdatedBy", sa.VARCHAR(length=100), autoincrement=False, nullable=True
        ),
        sa.Column("User Id", sa.UUID(), autoincrement=False, nullable=False),
    )
    op.create_index("ix_users_UserId", "users", ["User Id"], unique=False)
    op.create_index("ix_users_Email", "users", ["Email"], unique=True)
    op.create_index("idx_email_active", "users", ["Email", "IsActive"], unique=False)
