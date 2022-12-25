from datetime import datetime, timezone

from src.core.services import app as app_services
from src.services.unit_of_work import UnitOfWork


async def create_app(uow: UnitOfWork, project_id: str, plan: str, app_name: str):
    """Create a new app."""
    created_at = datetime.now(tz=timezone.utc)
    async with uow:
        current_app = await uow.apps.get(app_name)
        if current_app:
            raise ValueError(f"App {app_name} already exists")
        app = app_services.create_app(project_id, plan, app_name, created_at)
        await uow.apps.add(app)
        await uow.commit()
        return app
