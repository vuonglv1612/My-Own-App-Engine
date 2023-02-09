from sqlalchemy import Table, Column, String, Integer

from utils.datetime import naive_now
from .base import metadata, TimeStamp


SubscriptionItemsTable = Table(
    "subscription_items",
    metadata,
    Column("id", String(32), primary_key=True),
    Column("created_at", TimeStamp(), index=True, default=naive_now),
    Column("deleted_at", TimeStamp()),
    Column("sub_id", String(32)),
    Column("price_id", String(32)),
    Column("quantity", Integer),
)
