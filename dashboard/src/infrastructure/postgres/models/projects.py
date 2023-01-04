import uuid

from sqlalchemy import Column, String, Table, Integer, Boolean

from src.utils.datetime import naive_now
from .base import metadata, TimeStamp

ProjectTable = Table(
    "projects",
    metadata,
    Column("id", String(32), primary_key=True, default=lambda: str(uuid.uuid4().hex)),
    Column("name", String(255)),
    Column("created_at", TimeStamp(), index=True, default=naive_now),
    Column("deleted_at", TimeStamp(), index=True),
    Column("deleted", Boolean, default=False),
    Column("suspended", Boolean, default=False),
    Column("version_number", Integer, default=1),
)
