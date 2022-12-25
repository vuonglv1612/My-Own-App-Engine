from datetime import datetime

from attrs import define, field

APP_CREATED = "created"
APP_DELETED = "deleted"


@define
class App:
    name: str
    organization_id: str
    status: str
    created_at: datetime = field(default=None)
    deleted_at: datetime = field(init=False, default=None)

    @classmethod
    def create(cls, organization_id: str, app_name: str, created_at: datetime):
        return cls(organization_id=organization_id, name=app_name, status=APP_CREATED, created_at=created_at)

    def delete(self, deleted_at: datetime):
        self.status = APP_DELETED
        self.deleted_at = deleted_at
