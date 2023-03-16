import uuid

from sqlalchemy import Table, Column, String, ForeignKeyConstraint, Text

from src.infrastructure.postgres.models import metadata

EnvironmentTable = Table(
    "environments",
    metadata,
    Column("id", String(255), primary_key=True, default=lambda: str(uuid.uuid4().hex)),
    Column("app_id", String(255), index=True),
    Column("name", String(255)),
    Column("value", Text),
    ForeignKeyConstraint(("app_id",), ("apps.id",)),
)
