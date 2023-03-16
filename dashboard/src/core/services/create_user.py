import random
import time
from typing import Optional

from attrs import define, field

from src.core.entities import Project
from src.core.entities.project import ProjectMember
from src.core.entities.users import User


@define(kw_only=True, slots=False)
class CreateUserCommand:
    sub: str
    email: str
    name: Optional[str] = field(default=None)


class CreateUserUserCase:
    def __init__(self, uow, billing_client):
        self._uow = uow
        self._billing_client = billing_client

    @staticmethod
    def _create_random_name():
        return random.choice(["John", "Jane", "Bob", "Alice", "Tom", "Jerry"]) + str(int(time.time()))

    async def execute(self, command: CreateUserCommand):
        name = command.name or self._create_random_name()
        account_id = await self._billing_client.create_account(name=name)
        user = User(
            id=str(command.sub),
            name=name,
            email=command.email,
        )
        project = Project(
            name=name,
            account_id=account_id,
        )
        project_member = ProjectMember(
            role="owner",
        )
        project_member.project = project
        project_member.user = user
        async with self._uow:
            await self._uow.project_members.add(project_member)
            await self._uow.commit()
        return user
