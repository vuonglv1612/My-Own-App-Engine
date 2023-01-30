from sqlalchemy import Table, String, Column, ForeignKey, Boolean
from sqlalchemy.dialects.postgresql import JSONB

from utils.datetime import aware_now
from .base import metadata, TimeStamp

PriceTable = Table(
    "prices",
    metadata,
    Column("id", String(32), primary_key=True),
    Column("product_id", String(32), ForeignKey("products.id"), nullable=False),
    Column("created_at", TimeStamp(), default=aware_now),
    Column("active", Boolean, default=True),
    Column("lookup_key", String, nullable=True),
    Column("tiers_mode", String, default="graduated"),
    Column("recurring", JSONB, nullable=False),
    Column("tiers", JSONB, nullable=False),
)
