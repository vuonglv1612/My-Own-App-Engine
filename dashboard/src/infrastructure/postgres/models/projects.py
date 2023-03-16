import uuid

from sqlalchemy import Column, String, Table, Integer, Boolean
from sqlalchemy import ForeignKeyConstraint

from src.utils.datetime import naive_now
from .base import metadata, TimeStamp

ProjectTable = Table(
    "projects",
    metadata,
    Column("id", String(255), primary_key=True, default=lambda: str(uuid.uuid4().hex)),
    Column("name", String(255)),
    Column("account_id", String(255)),
    Column("created_at", TimeStamp(), index=True, default=naive_now),
    Column("deleted_at", TimeStamp(), index=True),
    Column("deleted", Boolean, default=False),
    Column("suspended", Boolean, default=False),
    Column("version_number", Integer, default=1),
)

ProjectMemberTable = Table(
    "project_members",
    metadata,
    Column("id", String(255), primary_key=True, default=lambda: str(uuid.uuid4().hex)),
    Column("project_id", String(255), index=True),
    Column("user_id", String(255), index=True),
    Column("created_at", TimeStamp(), index=True, default=naive_now),
    Column("role", String(255)),
    ForeignKeyConstraint(["project_id"], ["projects.id"]),
    ForeignKeyConstraint(["user_id"], ["users.id"]),
)
