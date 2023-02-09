from datetime import timedelta
from sqlalchemy import Table, String, Column, ForeignKey, Boolean, Float, Integer
from sqlalchemy import func
from sqlalchemy.dialects.postgresql import JSONB

from utils.datetime import aware_now, naive_now
from .base import metadata, TimeStamp


InvoiceTable = Table(
    "invoices",
    metadata,
    Column("id", String(32), primary_key=True),
    Column("sub_id", String(32), nullable=False),
    Column("account_id", String(32), nullable=False),
    Column("created_at", TimeStamp(), index=True, default=naive_now),
    Column("deleted_at", TimeStamp()),
    Column("due", TimeStamp(), default=func.now() + timedelta(days=3)),
    Column("status", String, default="open"),
    Column("account_address", String, nullable=True),
    Column("account_email", String, nullable=True),
    Column("period_start", Integer, nullable=False),
    Column("period_end", Integer, nullable=False),
    Column("amount", Float, nullable=False)
)
