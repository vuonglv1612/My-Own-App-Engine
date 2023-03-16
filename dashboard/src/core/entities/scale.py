import uuid
from datetime import datetime
from typing import Optional

from attrs import define, field

from src.utils.datetime import aware_now


@define(kw_only=True, slots=False)
class Unit:
    id: str = field()
    cpu: int = field()
    memory: int = field()
    plan_name: str = field()
    active: bool = field()
    created_at: datetime = field(factory=aware_now)
    deleted_at: Optional[datetime] = field(default=None)


@define(kw_only=True, slots=False)
class Scale:
    id: str = field(factory=lambda: str(uuid.uuid4().hex))
    app_id: str = field()
    unit_id: str = field()
    start_time: datetime = field()
    replicas: int = field(default=1)
    created_at: datetime = field(factory=aware_now)
    deleted_at: Optional[datetime] = field(default=None)
    end_time: Optional[datetime] = field(default=None)
    active: bool = field(default=True)
    unit: Optional[Unit] = field(default=None)
