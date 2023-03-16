import json

from attrs import define, field, asdict

from src.core.entities import App, Activity, User, Scale
from src.services.provisioner import Provisioner
from src.services.unit_of_work import UnitOfWork


def platform_validator(_, __, value):
    if value not in ["go", "python", "static", "buildpack"]:
        raise ValueError("Nền tảng không hợp lệ")


@define(kw_only=True, slots=False)
class CreateAppCommand:
    user: User = field()
    name: str = field()
    platform: str = field(validator=platform_validator)
    project_id: str = field()
    unit: str = field()
    replicas: int = field(default=1)
    description: str = field(default="")


class CreateAppUseCase:
    def __init__(self, uow: UnitOfWork, provisioner: Provisioner):
        self.uow = uow
        self.provisioner = provisioner

    async def handle(self, command: CreateAppCommand):
        async with self.uow:
            project = await self.uow.projects.get_by_id(command.project_id)
            if not project:
                raise ValueError("Project not found")
            unit = await self.uow.units.get_by_id(command.unit)
            if not unit:
                raise ValueError("Unit not found")
            await self.provisioner.create_app(app_name=command.name, platform=command.platform, plan=unit.plan_name)
            app = App(
                id=command.name.lower(),
                name=command.name,
                project_id=command.project_id,
                platform=command.platform,
                description=command.description,
            )
            app.status = "created"
            scale = Scale(
                app_id=app.id,
                unit_id=unit.id,
                replicas=command.replicas,
                start_time=app.created_at
            )
            scale.unit = unit
            activity = Activity(
                actor=json.loads(json.dumps(asdict(command.user), default=str)),
                event_type="app.created",
                event="Ứng dụng đã được tạo",
            )
            activity.app = app
            await self.uow.apps.add(app)
            await self.uow.activities.add(activity)
            await self.uow.scales.add(scale)
            await self.uow.commit()
        return app
