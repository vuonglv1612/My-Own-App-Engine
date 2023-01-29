from sqlalchemy import Table, Column, String, Integer

from utils.datetime import naive_now
from .base import metadata, TimeStamp

ProductTable = Table(
    "products",
    metadata,
    Column("id", String(32), primary_key=True),
    Column("created_at", TimeStamp(), index=True, default=naive_now),
    Column("deleted_at", TimeStamp()),
    Column("name", String(255)),
    Column("description", String(255)),
    Column("unit_label", String(255)),
    Column("version_number", Integer),
)
