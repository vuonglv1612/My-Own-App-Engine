import uuid

from sqlalchemy import Column, String, Table, DateTime, ForeignKeyConstraint

from src.utils import naive_now
from .base import metadata

SubscriptionTable = Table(
    "subscriptions",
    metadata,
    Column("id", String(32), primary_key=True, index=True, default=lambda: str(uuid.uuid4().hex)),
    Column("project_id", String(32), index=True),
    Column("plan_id", String(32), index=True),
    Column("billing_cycle", String(32), index=True),
    Column("status", String(32)),
    Column("cycle_started_at", DateTime, index=True),
    Column("cycle_ends_at", DateTime, index=True),
    Column("created_at", DateTime, index=True, default=naive_now),
    Column("deleted_at", DateTime, index=True),
    ForeignKeyConstraint(
        ("project_id",),
        ("projects.id",),
        ondelete="CASCADE",
    ),
    ForeignKeyConstraint(
        ("plan_id",),
        ("plans.id",),
    ),
)
