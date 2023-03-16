from datetime import datetime
from typing import Optional

from attrs import define, field

from src.utils.datetime import aware_now

APP_CREATED = "created"
APP_DELETED = "deleted"
APP_RUNNING = "running"
APP_STOPPED = "stopped"


@define(slots=False, kw_only=True)
class App:
    id: str
    name: str
    project_id: str
    status: str = field(init=False, default=APP_CREATED)
    platform: str
    description: Optional[str] = field(default=None)
    created_at: Optional[datetime] = field(default=aware_now)
    deleted_at: Optional[datetime] = field(default=None)
    version_number: int = field(init=False, default=1)
    activities: list['Activity'] = field(init=False, default=[])
    environments: list['Environment'] = field(init=False, default=[])

    def stop(self):
        if self.status == APP_CREATED:
            raise ValueError("Ứng dụng chưa được triển khai")
        self.status = APP_STOPPED

    def run(self):
        self.status = APP_RUNNING
