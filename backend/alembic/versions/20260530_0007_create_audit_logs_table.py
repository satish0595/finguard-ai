"""create audit_logs table

Revision ID: 0007
Revises: 0006
Create Date: 2026-05-31

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "0007"
down_revision: Union[str, None] = "0006"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "audit_logs",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column(
            "entity_type",
            sa.Enum(
                "user", "customer", "transaction", "alert", "case", "document",
                name="entity_type", native_enum=False
            ),
            nullable=False,
        ),
        sa.Column("entity_id", sa.Uuid(), nullable=False),
        sa.Column(
            "action",
            sa.Enum(
                "create", "read", "update", "delete",
                name="audit_action", native_enum=False
            ),
            nullable=False,
        ),
        sa.Column(
            "performed_by",
            sa.Uuid(),
            sa.ForeignKey("users.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column(
            "performed_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("old_values", sa.JSON(), nullable=True),
        sa.Column("new_values", sa.JSON(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_audit_logs_entity_type"), "audit_logs", ["entity_type"])
    op.create_index(op.f("ix_audit_logs_entity_id"), "audit_logs", ["entity_id"])
    op.create_index(op.f("ix_audit_logs_performed_by"), "audit_logs", ["performed_by"])
    op.create_index(op.f("ix_audit_logs_performed_at"), "audit_logs", ["performed_at"])


def downgrade() -> None:
    op.drop_index(op.f("ix_audit_logs_performed_at"), table_name="audit_logs")
    op.drop_index(op.f("ix_audit_logs_performed_by"), table_name="audit_logs")
    op.drop_index(op.f("ix_audit_logs_entity_id"), table_name="audit_logs")
    op.drop_index(op.f("ix_audit_logs_entity_type"), table_name="audit_logs")
    op.drop_table("audit_logs")
