"""create customers table

Revision ID: 0002
Revises: 0001
Create Date: 2026-05-30

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "0002"
down_revision: Union[str, None] = "0001"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "customers",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("external_reference", sa.String(length=64), nullable=False),
        sa.Column("legal_name", sa.String(length=255), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=True),
        sa.Column("phone", sa.String(length=32), nullable=True),
        sa.Column(
            "customer_type",
            sa.Enum(
                "individual",
                "business",
                name="customer_type",
                native_enum=False,
            ),
            nullable=False,
        ),
        sa.Column(
            "risk_level",
            sa.Enum(
                "low",
                "medium",
                "high",
                "unknown",
                name="risk_level",
                native_enum=False,
            ),
            nullable=False,
        ),
        sa.Column(
            "status",
            sa.Enum(
                "active",
                "inactive",
                "pending_review",
                "closed",
                name="customer_status",
                native_enum=False,
            ),
            nullable=False,
        ),
        sa.Column("country_code", sa.String(length=2), nullable=True),
        sa.Column("date_of_birth", sa.Date(), nullable=True),
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
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_customers_external_reference"),
        "customers",
        ["external_reference"],
        unique=True,
    )


def downgrade() -> None:
    op.drop_index(
        op.f("ix_customers_external_reference"), table_name="customers"
    )
    op.drop_table("customers")
