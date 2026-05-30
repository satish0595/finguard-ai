"""create transactions table

Revision ID: 0003
Revises: 0002
Create Date: 2026-05-30

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "0003"
down_revision: Union[str, None] = "0002"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "transactions",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("customer_id", sa.Uuid(), nullable=False),
        sa.Column("external_reference", sa.String(length=64), nullable=False),
        sa.Column("amount", sa.Numeric(precision=18, scale=2), nullable=False),
        sa.Column("currency", sa.String(length=3), nullable=False),
        sa.Column(
            "transaction_type",
            sa.Enum(
                "payment",
                "transfer",
                "withdrawal",
                "deposit",
                "wire",
                name="transaction_type",
                native_enum=False,
            ),
            nullable=False,
        ),
        sa.Column(
            "direction",
            sa.Enum(
                "inbound",
                "outbound",
                name="transaction_direction",
                native_enum=False,
            ),
            nullable=False,
        ),
        sa.Column(
            "status",
            sa.Enum(
                "pending",
                "completed",
                "failed",
                "reversed",
                name="transaction_status",
                native_enum=False,
            ),
            nullable=False,
        ),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("counterparty_name", sa.String(length=255), nullable=True),
        sa.Column("transaction_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["customer_id"],
            ["customers.id"],
            ondelete="RESTRICT",
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_transactions_customer_id"),
        "transactions",
        ["customer_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_transactions_external_reference"),
        "transactions",
        ["external_reference"],
        unique=True,
    )


def downgrade() -> None:
    op.drop_index(
        op.f("ix_transactions_external_reference"), table_name="transactions"
    )
    op.drop_index(op.f("ix_transactions_customer_id"), table_name="transactions")
    op.drop_table("transactions")
