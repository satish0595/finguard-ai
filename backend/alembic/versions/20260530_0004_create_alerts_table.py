"""create alerts table

Revision ID: 0004
Revises: 0003
Create Date: 2026-05-30

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "0004"
down_revision: Union[str, None] = "0003"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "alerts",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("external_reference", sa.String(length=64), nullable=False),
        sa.Column("customer_id", sa.Uuid(), nullable=False),
        sa.Column("transaction_id", sa.Uuid(), nullable=True),
        sa.Column("assigned_to", sa.Uuid(), nullable=True),
        sa.Column(
            "alert_type",
            sa.Enum(
                "sanctions_hit",
                "unusual_activity",
                "threshold_breach",
                "manual_review",
                "pep_match",
                name="alert_type",
                native_enum=False,
            ),
            nullable=False,
        ),
        sa.Column(
            "severity",
            sa.Enum(
                "low",
                "medium",
                "high",
                "critical",
                name="alert_severity",
                native_enum=False,
            ),
            nullable=False,
        ),
        sa.Column(
            "status",
            sa.Enum(
                "open",
                "investigating",
                "escalated",
                "closed",
                "false_positive",
                name="alert_status",
                native_enum=False,
            ),
            nullable=False,
        ),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("triggered_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("resolved_at", sa.DateTime(timezone=True), nullable=True),
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
            ["transaction_id"],
            ["transactions.id"],
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
        op.f("ix_alerts_external_reference"),
        "alerts",
        ["external_reference"],
        unique=True,
    )
    op.create_index(op.f("ix_alerts_customer_id"), "alerts", ["customer_id"])
    op.create_index(op.f("ix_alerts_transaction_id"), "alerts", ["transaction_id"])
    op.create_index(op.f("ix_alerts_assigned_to"), "alerts", ["assigned_to"])


def downgrade() -> None:
    op.drop_index(op.f("ix_alerts_assigned_to"), table_name="alerts")
    op.drop_index(op.f("ix_alerts_transaction_id"), table_name="alerts")
    op.drop_index(op.f("ix_alerts_customer_id"), table_name="alerts")
    op.drop_index(op.f("ix_alerts_external_reference"), table_name="alerts")
    op.drop_table("alerts")
