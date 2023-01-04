import uuid

from sqlalchemy import Column, String, Table, ForeignKeyConstraint, Integer

from src.utils.datetime import naive_now
from .base import metadata, TimeStamp

AppTable = Table(
    "apps",
    metadata,
    Column("id", String(32), primary_key=True, default=lambda: str(uuid.uuid4().hex)),
    Column("name", String(255)),
    Column("project_id", String(32), index=True),
    Column("plan_id", String(32), index=True),
    Column("status", String(32)),
    Column("created_at", TimeStamp(), index=True, default=naive_now),
    Column("deleted_at", TimeStamp(), index=True),
    Column("version_number", Integer, default=1),
    ForeignKeyConstraint(("project_id",), ("projects.id",)),
    ForeignKeyConstraint(("plan_id",), ("plans.id",)),
)
