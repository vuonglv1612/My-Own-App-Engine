from datetime import datetime
from typing import Optional

from attrs import define, field

from utils.datetime import aware_now


@define(kw_only=True, slots=False)
class Subscription:
    id: str = field()
    created_at: datetime = field(factory=aware_now)
    deleted_at: datetime = field(factory=aware_now)
    account_id: str = field()
    current_period_start: int = field()
    current_period_end: int = field()
    cancel_at: Optional[int] = field(default=None)
    cancelled: bool = field(default=False)
    status: str = field(default="active")
    current_period_amount: float = field(default=0)


@define(kw_only=True, slots=False)
class SubscriptionItem:
    id: str = field()
    created_at: datetime = field(factory=aware_now)
    deleted_at: datetime = field(factory=aware_now)
    sub_id: str = field()
    price_id: str = field()
    quantity: int = field(default=0)
