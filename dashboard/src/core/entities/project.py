import uuid
from datetime import datetime
from typing import Optional

from attrs import define, field


@define(kw_only=True, slots=False)
class ProjectMember:
    id: str = field(factory=lambda: str(uuid.uuid4().hex))
    project_id: Optional[str] = field(default=None)
    user_id: Optional[str] = field(default=None)
    role: str
    created_at: datetime = field(default=None)


@define(kw_only=True, slots=False)
class Project:
    id: str = field(factory=lambda: str(uuid.uuid4().hex))
    name: str
    account_id: str
    created_at: datetime = field(default=None)
    deleted_at: datetime = field(init=False, default=None)
    deleted: bool = field(init=False, default=False)
    suspended: bool = field(init=False, default=False)
    version_number: int = field(init=False, default=1)
    members: list[ProjectMember] = field(init=False, default=[])

    def is_member(self, user_id: str) -> bool:
        return any(member.user_id == user_id for member in self.members)

    def is_admin(self, user_id: str) -> bool:
        return any(member.user_id == user_id and member.role in ["admin", "owner"] for member in self.members)

    def is_owner(self, user_id: str) -> bool:
        return any(member.user_id == user_id and member.role == "owner" for member in self.members)
