import uuid

from sqlalchemy import Table, Column, String, ForeignKeyConstraint, Text

from src.infrastructure.postgres.models.base import TimeStamp, metadata
from src.utils.datetime import naive_now

DeploymentTable = Table(
    "deployments",
    metadata,
    Column("id", String(255), primary_key=True, default=lambda: str(uuid.uuid4().hex)),
    Column("app_id", String(255), index=True),
    Column("scale_id", String(255), index=True),
    Column("created_at", TimeStamp(), index=True, default=naive_now),
    Column("deleted_at", TimeStamp(), index=True),
    Column("source_url", Text, nullable=False),
    Column("source_type", Text, nullable=False),
    Column("image_url", Text),
    Column("image_registry", Text),
    Column("image_tag", String(255)),
    Column("status", String(255)),
    ForeignKeyConstraint(("app_id",), ("apps.id",)),
    ForeignKeyConstraint(("scale_id",), ("scales.id",)),
)
