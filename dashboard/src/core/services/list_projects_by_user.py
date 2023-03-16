from attrs import define


@define(kw_only=True, slots=False)
class ListProjectByUserCommand:
    user_id: str
    page: int
    per_page: int


class ListProjectByUserUseCase:
    def __init__(self, uow):
        self._uow = uow

    async def execute(self, command: ListProjectByUserCommand):
        async with self._uow:
            total, projects = await self._uow.projects.list_by_user(command.user_id, command.page, command.per_page)
            return {"items": projects, "meta": {"total": total, "page": command.page, "per_page": command.per_page}}
