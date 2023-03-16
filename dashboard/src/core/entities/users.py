import uuid
from datetime import datetime
from typing import Optional

from attrs import define, field


@define(kw_only=True, slots=False)
class User:
    id: str = field(factory=lambda: str(uuid.uuid4().hex))
    name: str
    email: str
    created_at: datetime = field(factory=datetime.utcnow)
    deleted_at: Optional[datetime] = None
    deleted: bool = False
