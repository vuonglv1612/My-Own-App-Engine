import uuid

from sqlalchemy import Column, String, Table, Boolean

from src.utils.datetime import naive_now
from .base import metadata, TimeStamp

PlanTable = Table(
    "plans",
    metadata,
    Column("id", String(32), primary_key=True, default=lambda: str(uuid.uuid4().hex)),
    Column("lookup_key", String(255), unique=True, index=True),
    Column("display_name", String(255)),
    Column("price_id", String(255), index=True),
    Column("active", Boolean, default=True),
    Column("created_at", TimeStamp(), index=True, default=naive_now),
    Column("deleted_at", TimeStamp(), index=True),
)
