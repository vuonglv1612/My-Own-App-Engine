from datetime import datetime

from attrs import define, field

APP_CREATED = "created"
APP_DELETED = "deleted"


@define(slots=False)
class App:
    id: str
    name: str
    project_id: str
    plan_id: str
    status: str
    created_at: datetime = field(default=None)
    deleted_at: datetime = field(init=False, default=None)
    deleted: bool = field(init=False, default=False)
    version_number: int = field(init=False, default=1)

    @classmethod
    def create(cls, project_id: str, plan_id: str, app_name: str, created_at: datetime):
        return cls(
            id=app_name,
            project_id=project_id,
            plan_id=plan_id,
            name=app_name,
            status=APP_CREATED,
            created_at=created_at,
        )

    def delete(self, deleted_at: datetime):
        self.status = APP_DELETED
        self.deleted = True
        self.deleted_at = deleted_at
