from sqlalchemy import Column, String, Table, ForeignKeyConstraint, Integer, Float

from utils.datetime import naive_now
from .base import metadata, TimeStamp

AccountBalanceTable = Table(
    "account_balances",
    metadata,
    Column("id", String(32), primary_key=True),
    Column("created_at", TimeStamp(), index=True, default=naive_now),
    Column("amount", Float, default=0.0),
    Column("account_id", String(32), index=True),
    Column("version_number", Integer, default=1),
    ForeignKeyConstraint(("account_id",), ("accounts.id",)),
)

TransactionTable = Table(
    "transactions",
    metadata,
    Column("id", String(32), primary_key=True),
    Column("created_at", TimeStamp(), index=True, default=naive_now),
    Column("balance_id", String(32), index=True),
    Column("account_id", String(32), index=True),
    Column("amount", Float),
    Column("transaction_type", String(32)),
    Column("description", String(255)),
    ForeignKeyConstraint(("balance_id",), ("account_balances.id",)),
)
