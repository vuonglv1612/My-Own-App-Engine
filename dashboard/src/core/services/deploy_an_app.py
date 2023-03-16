import json

from attrs import define, field, asdict

from src.core.entities import Activity, User, Deployment
from src.core.error import InternalError
from src.services.build_client import DeployClient
from src.services.unit_of_work import UnitOfWork


@define(slots=False, kw_only=True)
class DeployAppCommand:
    user: User = field()
    version: str = field()
    project_id: str = field()
    app_id: str = field()
    source_type: str = field()
    source_url: str = field()
    git_branch: str = field(default="master")


class DeployAppUseCase:
    def __init__(self, uow: UnitOfWork, deploy_client: DeployClient):
        self.uow = uow
        self.deploy_client = deploy_client

    async def handle(self, command: DeployAppCommand):
        async with self.uow:
            project = await self.uow.projects.get_by_id(command.project_id)
            if not project:
                raise ValueError("Không tìm thấy dự án")
            is_member = project.is_member(command.user.id)
            if not is_member:
                raise ValueError("Bạn không có quyền truy cập")
            app = await self.uow.apps.get_by_name(app_name=command.app_id, project_id=command.project_id, active=True)
            if not app:
                raise ValueError("Không tìm thấy ứng dụng")
            # find active scale of app
            scale = await self.uow.scales.get_active_by_app_id(app_id=app.id)
            if not scale:
                raise InternalError("Scale not found")
            unit = await self.uow.units.get_by_id(scale.unit_id)
            app.status = "running"
            deployment = Deployment(
                app_id=app.id,
                source_type=command.source_type,
                source_url=command.source_url,
                status="pending",
                scale_id=scale.id,
            )
            activity = Activity(
                actor=json.loads(json.dumps(asdict(command.user), default=str)),
                event_type="app.deployed",
                event="Triển khai phiên bản mới",
            )
            activity.app = app
            await self.uow.apps.add(app)
            await self.uow.deployments.add(deployment)
            await self.uow.activities.add(activity)
            await self.uow.commit()
        if deployment.source_type == "git":
            await self.deploy_client.deploy_git_app(
                deployment_id=deployment.id,
                app_name=app.name,
                plan_name=unit.plan_name,
                git_url=deployment.source_url,
                git_branch=command.git_branch,
                replicas=scale.replicas
            )
        elif deployment.source_type == "image":
            await self.deploy_client.deploy_image_app(
                deployment_id=deployment.id,
                app_name=app.name,
                plan_name=unit.plan_name,
                image=deployment.source_url,
                replicas=scale.replicas
            )
        return deployment
