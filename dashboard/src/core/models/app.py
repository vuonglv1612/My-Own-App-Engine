from datetime import datetime

from attrs import define, field

APP_CREATED = "created"
APP_DELETED = "deleted"


@define
class App:
    id: str
    name: str
    project_id: str
    plan: str
    status: str
    created_at: datetime = field(default=None)
    deleted_at: datetime = field(init=False, default=None)

    @classmethod
    def create(cls, project_id: str, plan: str, app_name: str, created_at: datetime):
        return cls(
            id=app_name, project_id=project_id, plan=plan, name=app_name, status=APP_CREATED, created_at=created_at
        )

    def delete(self, deleted_at: datetime):
        self.status = APP_DELETED
        self.deleted_at = deleted_at
