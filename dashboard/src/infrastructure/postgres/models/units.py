# unit has id, cpu, memory, plan_name, price_id
import uuid

from sqlalchemy import Table, Column, String, Integer, Boolean, ForeignKeyConstraint

from src.infrastructure.postgres.models.base import TimeStamp, metadata
from src.utils.datetime import naive_now

UnitTable = Table(
    "units",
    metadata,
    Column("id", String(255), primary_key=True, default=lambda: str(uuid.uuid4().hex)),
    Column("cpu", Integer),
    Column("memory", Integer),
    Column("plan_name", String(255)),
    Column("price_id", String(255), index=True),
    Column("active", Boolean, default=True),
    Column("created_at", TimeStamp(), index=True, default=naive_now),
    Column("deleted_at", TimeStamp(), index=True),
)

ScaleTable = Table(
    "scales",
    metadata,
    Column("id", String(255), primary_key=True, default=lambda: str(uuid.uuid4().hex)),
    Column("app_id", String(255), index=True),
    Column("unit_id", String(255), index=True),
    Column("replicas", Integer),
    Column("created_at", TimeStamp(), index=True, default=naive_now),
    Column("deleted_at", TimeStamp(), index=True),
    Column("start_time", TimeStamp(), index=True),
    Column("end_time", TimeStamp(), index=True),
    Column("active", Boolean, default=True),
    ForeignKeyConstraint(("app_id",), ("apps.id",)),
    ForeignKeyConstraint(("unit_id",), ("units.id",)),
)
