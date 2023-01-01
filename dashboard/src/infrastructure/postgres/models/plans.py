import uuid

from sqlalchemy import Column, String, Table, DateTime

from src.utils import naive_now
from .base import metadata

PlanTable = Table(
    "plans",
    metadata,
    Column("id", String(32), primary_key=True, index=True, default=lambda: str(uuid.uuid4().hex)),
    Column("name", String(255), index=True),
    Column("created_at", DateTime, index=True, default=naive_now),
    Column("deleted_at", DateTime, index=True),
)
