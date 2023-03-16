import uuid

from sqlalchemy import Column, String, Table, ForeignKeyConstraint, Integer

from src.utils.datetime import naive_now
from .base import metadata, TimeStamp

AppTable = Table(
    "apps",
    metadata,
    Column("id", String(255), primary_key=True, default=lambda: str(uuid.uuid4().hex)),
    Column("name", String(255)),
    Column("project_id", String(255), index=True),
    Column("status", String(255)),
    Column("platform", String(255)),
    Column("description", String(255)),
    Column("created_at", TimeStamp(), index=True, default=naive_now),
    Column("deleted_at", TimeStamp(), index=True),
    Column("version_number", Integer, default=1),
    ForeignKeyConstraint(("project_id",), ("projects.id",)),
)
