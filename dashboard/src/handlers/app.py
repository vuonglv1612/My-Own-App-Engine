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
    plan: str,
    app_name: str,
    created_at: Optional[datetime] = None,
):
    """Create a new test_cases."""
    if not created_at:
        created_at = datetime.now(tz=timezone.utc)
    async with uow:
        current_app = await uow.apps.get(app_name)
        if current_app:
            raise ValueError(f"App {app_name} already exists")
        app = app_services.create_app(project_id, plan, app_name, created_at)
        await uow.apps.add(app)
        await uow.commit()
    await provisioner.create_app(project_id, app_name, plan)
    return asdict(app)
