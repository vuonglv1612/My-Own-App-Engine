import uuid

from sqlalchemy import Table, Column, String, ForeignKeyConstraint, JSON

from src.infrastructure.postgres.models.base import TimeStamp, metadata
from src.utils.datetime import naive_now

ActivityTable = Table(
    "activities",
    metadata,
    Column("id", String(255), primary_key=True, default=lambda: str(uuid.uuid4().hex)),
    Column("app_id", String(255), index=True),
    Column("actor", JSON),
    Column("event_type", String(255)),
    Column("event", String(255)),
    Column("created_at", TimeStamp(), index=True, default=naive_now),
    ForeignKeyConstraint(("app_id",), ("apps.id",)),
)
