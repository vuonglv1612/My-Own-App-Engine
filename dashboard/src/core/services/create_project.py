from attrs import define, field, asdict

from src.core.entities import Project, ProjectMember
from src.services.billing import BillingClient
from src.services.unit_of_work import UnitOfWork


@define(kw_only=True, slots=False)
class CreateProjectCommand:
    user_id: str = field()
    name: str = field()


class CreateProjectUseCase:
    def __init__(self, uow: UnitOfWork, billing_client: BillingClient):
        self.uow = uow
        self.billing_client = billing_client

    async def execute(self, command: CreateProjectCommand):
        async with self.uow:
            user = await self.uow.users.get_by_id(command.user_id)
            if not user:
                raise ValueError("User not found")
            if command.name == user.name:
                raise ValueError("Project name can not be same as user name")
            account_id = await self.billing_client.create_account(name=command.name)
            project = Project(
                name=command.name,
                account_id=account_id
            )
            member = ProjectMember(
                role="owner"
            )
            member.project = project
            member.user = user
            await self.uow.project_members.add(member)
            await self.uow.commit()
            return asdict(project)
