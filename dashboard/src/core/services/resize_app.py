from attrs import define, field

from src.core.entities import User, Scale
from src.services.build_client import DeployClient
from src.services.unit_of_work import UnitOfWork
from src.utils.datetime import aware_now


@define(slots=False, kw_only=True)
class ScaleAppCommand:
    user: User = field()
    app_id: str = field()
    replicas: int = field()


class ScaleAppUseCase:
    def __init__(self, uow: UnitOfWork, deploy_client: DeployClient):
        self.uow = uow
        self.deploy_client = deploy_client

    async def execute(self, command: ScaleAppCommand):
        async with self.uow:
            if command.replicas <= 0:
                raise ValueError("Replicas must be greater than 0")
            app = await self.uow.apps.get_by_id(command.app_id)
            if not app:
                raise ValueError("App not found")
            project = await self.uow.projects.get_by_id(app.project_id)
            if not project:
                raise ValueError("Project not found")
            is_member = project.is_member(command.user.id)
            if not is_member:
                raise ValueError("You are not a member of this project")
            current_active_scale = await self.uow.scales.get_active_by_app_id(command.app_id)
            if current_active_scale:
                current_active_scale.end_time = aware_now()
                current_active_scale.active = False
                await self.uow.scales.add(current_active_scale)
            change = command.replicas - current_active_scale.replicas
            if not change:
                raise ValueError("Replicas count is the same")

            scale = Scale(
                app_id=command.app_id,
                unit_id=current_active_scale.unit_id,
                replicas=command.replicas,
                start_time=aware_now(),
                active=True
            )
            scale.unit = current_active_scale.unit
            await self.uow.scales.add(scale)
            await self.uow.commit()
            await self.deploy_client.scale_app(app_name=command.app_id, change=change)
            return scale
