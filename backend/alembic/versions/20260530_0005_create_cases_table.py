"""create cases table

Revision ID: 0005
Revises: 0004
Create Date: 2026-05-30

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "0005"
down_revision: Union[str, None] = "0004"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "cases",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("external_reference", sa.String(length=64), nullable=False),
        sa.Column("customer_id", sa.Uuid(), nullable=False),
        sa.Column("alert_id", sa.Uuid(), nullable=True),
        sa.Column("assigned_to", sa.Uuid(), nullable=True),
        sa.Column(
            "priority",
            sa.Enum(
                "low",
                "medium",
                "high",
                "urgent",
                name="case_priority",
                native_enum=False,
            ),
            nullable=False,
        ),
        sa.Column(
            "status",
            sa.Enum(
                "open",
                "in_progress",
                "pending_info",
                "closed",
                "archived",
                name="case_status",
                native_enum=False,
            ),
            nullable=False,
        ),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("summary", sa.Text(), nullable=True),
        sa.Column("opened_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("closed_at", sa.DateTime(timezone=True), nullable=True),
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
        sa.ForeignKeyConstraint(
            ["alert_id"],
            ["alerts.id"],
            ondelete="SET NULL",
        ),
        sa.ForeignKeyConstraint(
            ["assigned_to"],
            ["users.id"],
            ondelete="SET NULL",
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_cases_external_reference"),
        "cases",
        ["external_reference"],
        unique=True,
    )
    op.create_index(op.f("ix_cases_customer_id"), "cases", ["customer_id"])
    op.create_index(op.f("ix_cases_alert_id"), "cases", ["alert_id"])
    op.create_index(op.f("ix_cases_assigned_to"), "cases", ["assigned_to"])


def downgrade() -> None:
    op.drop_index(op.f("ix_cases_assigned_to"), table_name="cases")
    op.drop_index(op.f("ix_cases_alert_id"), table_name="cases")
    op.drop_index(op.f("ix_cases_customer_id"), table_name="cases")
    op.drop_index(op.f("ix_cases_external_reference"), table_name="cases")
    op.drop_table("cases")
