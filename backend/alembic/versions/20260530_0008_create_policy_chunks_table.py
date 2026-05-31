"""create policy_chunks table

Revision ID: 0008
Revises: 0007
Create Date: 2026-05-31

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "0008"
down_revision: Union[str, None] = "0007"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "policy_chunks",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("external_reference", sa.String(length=64), nullable=False),
        sa.Column("policy_name", sa.String(length=255), nullable=False),
        sa.Column("chunk_index", sa.Integer(), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("tags", sa.JSON(), nullable=True),
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
        sa.UniqueConstraint("external_reference", name="uq_policy_chunks_external_reference"),
    )
    op.create_index(op.f("ix_policy_chunks_policy_name"), "policy_chunks", ["policy_name"])
    op.create_index(op.f("ix_policy_chunks_chunk_index"), "policy_chunks", ["chunk_index"])


def downgrade() -> None:
    op.drop_index(op.f("ix_policy_chunks_chunk_index"), table_name="policy_chunks")
    op.drop_index(op.f("ix_policy_chunks_policy_name"), table_name="policy_chunks")
    op.drop_table("policy_chunks")
