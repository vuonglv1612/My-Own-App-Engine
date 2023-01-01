import uuid

from sqlalchemy import Column, String, Table, DateTime, DECIMAL, Text, ForeignKeyConstraint

from src.utils import naive_now
from .base import metadata

ProjectTable = Table(
    "projects",
    metadata,
    Column("id", String(32), primary_key=True, index=True, default=lambda: str(uuid.uuid4().hex)),
    Column("name", String(255)),
    Column("created_at", DateTime, index=True, default=naive_now),
    Column("deleted_at", DateTime, index=True),
)


BalanceAdjustmentTable = Table(
    "balance_adjustments",
    metadata,
    Column("id", String(32), primary_key=True, index=True, default=lambda: str(uuid.uuid4().hex)),
    Column("project_id", String(32), index=True),
    Column("amount", DECIMAL),
    Column("note", Text),
    Column("created_at", DateTime, index=True, default=naive_now),
    Column("deleted_at", DateTime, index=True),
    ForeignKeyConstraint(
        ("project_id",),
        ("projects.id",),
        ondelete="CASCADE",
    ),
)
