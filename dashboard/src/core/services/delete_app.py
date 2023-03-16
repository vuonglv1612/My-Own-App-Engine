from attrs import define, field

from src.core.entities import User


@define(kw_only=True, slots=False)
class DeleteAppCommand:
    user: User = field()
    app_id: str = field()


class DeleteAppUseCase:
    def __init__(self, uow, provisioner):
        self._uow = uow
        self._provisioner = provisioner

    async def handle(self, command: DeleteAppCommand):
        async with self._uow:
            app = await self._uow.apps.get_by_id(command.app_id)
            if not app:
                raise ValueError("Không tìm thấy ứng dụng")
            project = await self._uow.projects.get_by_id(app.project_id)
            if not project:
                raise ValueError("Không tìm thấy dự án")
            await self._uow.apps.delete(app)
            await self._uow.commit()
        await self._provisioner.delete_app(app_name=app.name)
