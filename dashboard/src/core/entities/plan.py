from datetime import datetime

from attrs import define, field

from src.utils.datetime import naive_now


@define(kw_only=True, slots=False)
class Plan:
    id: str
    lookup_key: str
    display_name: str
    price_id: str
    active: bool
    created_at: datetime = field(default=lambda: naive_now)
    deleted_at: datetime = field(init=False, default=None)
