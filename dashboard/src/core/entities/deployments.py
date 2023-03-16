import uuid
from datetime import datetime
from typing import Optional

from attrs import define, field

from src.utils.datetime import aware_now


@define(slots=False, kw_only=True)
class Deployment:
    id: str = field(factory=lambda: str(uuid.uuid4().hex))
    app_id: str
    scale_id: str
    source_url: str
    source_type: str
    image_url: Optional[str] = field(default=None)
    image_registry: Optional[str] = field(default=None)
    image_tag: Optional[str] = field(default=None)
    created_at: datetime = field(factory=aware_now)
    deleted_at: Optional[datetime] = field(default=None)
    status: str
