from datetime import datetime, timezone
from typing import Optional

from attrs import asdict

from src.core.services import app as app_services
from src.services.provisioner import Provisioner
from src.services.unit_of_work import UnitOfWork


async def new_app(
    uow: UnitOfWork,
    provisioner: Provisioner,
    project_id: str,
    plan_name: str,
    app_name: str,
    created_at: Optional[datetime] = None,
):
    """Create a new app."""
    if not created_at:
        created_at = datetime.now(tz=timezone.utc)
    async with uow:
        current_app = await uow.apps.get(app_name)
        if current_app:
            raise ValueError(f"App {app_name} already exists")
        project = await uow.projects.get(project_id)
        if not project:
            raise ValueError(f"Project {project_id} does not exist")
        plan = await uow.plans.get(plan_name)
        if not plan:
            raise ValueError(f"Plan {plan_name} does not exist")
        app = app_services.create_app(project_id, app_name, created_at)
        billing_resource = project.add_billing_resource(
            resource_id=app.id, resource_type="app", created_at=created_at, plan=plan
        )
        await uow.billing_resources.add(billing_resource)
        await uow.projects.add(project)
        await uow.apps.add(app)
        await uow.commit()
    await provisioner.create_app(project_id, app_name, plan_name)
    return asdict(app)
