from datetime import datetime
from typing import Optional

from attrs import define, field

from utils.datetime import aware_now


@define(kw_only=True, slots=False)
class Product:
    id: str = field()
    created_at: datetime = field(factory=aware_now)
    name: Optional[str] = field(default=None)
    description: Optional[str] = field(default=None)
    unit_label: Optional[str] = field(default=None)
    version_number: int = field(default=1)
