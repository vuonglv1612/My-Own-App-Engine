import uuid
from datetime import datetime
from typing import Any, Dict, Optional

from attrs import define, field


@define(slots=False, kw_only=True)
class Activity:
    id: str = field(factory=lambda: str(uuid.uuid4().hex))
    app_id: Optional[str] = field(default=None)
    actor: Dict[str, Any]
    event_type: str
    event: str
    created_at: datetime = field(default=None)
    app: 'App' = field(init=False, default=None)
