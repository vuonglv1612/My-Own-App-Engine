from sqlalchemy import Table, Column, String, Integer, Boolean, Float

from utils.datetime import naive_now
from .base import metadata, TimeStamp

SubscriptionTable = Table(
    "subscription",
    metadata,
    Column("id", String(32), primary_key=True),
    Column("created_at", TimeStamp(), index=True, default=naive_now),
    Column("deleted_at", TimeStamp()),
    Column("account_id", String(32)),
    Column("current_period_start", Integer),
    Column("current_period_end", Integer),
    Column("cancel_at", Integer),
    Column("cancelled", Boolean, default=False),
    Column("status", String(255)),
    Column("current_period_amount", Float)
)

