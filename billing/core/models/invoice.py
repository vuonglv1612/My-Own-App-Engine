from datetime import datetime, timedelta
from typing import List, Optional

from attrs import define, field

from utils.datetime import aware_now


@define(kw_only=True, slots=False)
class InvoiceLine:
    id: str = field()
    created_at: datetime = field(factory=aware_now)
    deleted_at: datetime = field(factory=aware_now)
    invoice_id: str = field()
    sub_item_id: str = field()
    price_id: str = field()
    quantity: int = field()
    description: str = field()
    amount: float = field()


@define(kw_only=True, slots=False)
class Invoice:
    id: str = field()
    created_at: datetime = field(factory=aware_now)
    deleted_at: datetime = field(factory=aware_now)
    sub_id: str = field()
    account_id: str = field()
    due: datetime = field(factory=lambda: aware_now() + timedelta(days=3))
    status: str = field(default="open")
    account_address: str = field(default=None)
    account_email: str = field(default=None)
    amount: float = field()
    period_start: int = field()
    period_end: int = field()

