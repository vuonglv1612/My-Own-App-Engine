from datetime import datetime

from attrs import define, field


@define(kw_only=True, slots=False)
class Project:
    id: str
    name: str
    created_at: datetime = field(default=None)
    deleted_at: datetime = field(init=False, default=None)
    deleted: bool = field(init=False, default=False)
    suspended: bool = field(init=False, default=False)
    version_number: int = field(init=False, default=1)
