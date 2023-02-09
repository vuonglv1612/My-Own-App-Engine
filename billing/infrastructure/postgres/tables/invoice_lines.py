from datetime import timedelta
from sqlalchemy import Table, String, Column, ForeignKey, Boolean, Float, Integer
from sqlalchemy import func
from sqlalchemy.dialects.postgresql import JSONB

from utils.datetime import aware_now, naive_now
from .base import metadata, TimeStamp


InvoiceLineTable = Table(
    "invoice_lines",
    metadata,
    Column("id", String(32), primary_key=True),
    Column("invoice_id", String(32), nullable=False),
    Column("created_at", TimeStamp(), index=True, default=naive_now),
    Column("deleted_at", TimeStamp()),
    Column("sub_item_id", String(32), nullable=False),
    Column("quantity", Integer),
    Column("price_id", String(32), nullable=False),
    Column("description", String(255)),
    Column("amount", Float, nullable=False)
)
