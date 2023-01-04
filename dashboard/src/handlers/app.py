from datetime import datetime, timezone

from attrs import asdict

from src.core.services import app as app_services
from src.services.unit_of_work import UnitOfWork


async def new_app(
    uow: UnitOfWork,
    project_id: str,
    app_name: str,
):
    """Create a new app."""
    created_at = datetime.now(tz=timezone.utc)
    async with uow:
        current_app = await uow.apps.get_by_name(app_name)
        if current_app:
            raise ValueError(f"App {app_name} already exists")
        project = await uow.projects.get_by_id(project_id)
        if not project:
            raise ValueError(f"Project {project_id} does not exist")
        plan = await uow.plans.get_current_plan()
        if not plan:
            raise Exception("No plan exists")
        app = app_services.create_app(project, plan, app_name, created_at)
        app_as_dict = asdict(app)
        await uow.apps.add(app)
        await uow.commit()
    return app_as_dict
