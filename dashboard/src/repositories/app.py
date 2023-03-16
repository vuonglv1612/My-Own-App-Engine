from abc import ABC, abstractmethod
from typing import Optional

from sqlalchemy import select, func
from sqlalchemy.orm import selectinload

from .base import SQLAlchemyRepository, IRepository
from ..core.entities import App


class AppRepository(IRepository[App], ABC):
    @abstractmethod
    async def get_by_name(self, app_name: str, project_id: str, active: bool = True) -> Optional[App]:
        raise NotImplementedError

    @abstractmethod
    async def list_app_in_project(self, project_id: str, page: int, page_size: int) -> (list[App], int):
        raise NotImplementedError

    async def delete(self, entity: App) -> None:
        raise NotImplementedError


class SQLAlchemyAppRepository(SQLAlchemyRepository[App], AppRepository):

    @staticmethod
    def _get_model():
        return App

    async def delete(self, entity: App) -> None:
        await self._session.delete(entity)

    async def get_by_name(self, app_name: str, project_id: str, active: bool = True) -> Optional[App]:
        statement = select(App).where(App.name == app_name, App.project_id == project_id)
        if active:
            statement = statement.where(App.deleted_at == None)
        result = await self._session.execute(statement)
        return result.scalars().first()

    async def list_app_in_project(self, project_id: str, page: int, page_size: int) -> (list[App], int):
        count_statement = select(func.count(App.id)).where(App.project_id == project_id)
        result = await self._session.execute(count_statement)
        total = result.scalar()
        statement = select(App).where(App.project_id == project_id).offset((page - 1) * page_size).limit(page_size)
        statement = statement.options(selectinload(App.activities), selectinload(App.environments))
        result = await self._session.execute(statement)
        apps = result.scalars().all()
        return apps, total
