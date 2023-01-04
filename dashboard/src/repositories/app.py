from abc import ABC, abstractmethod
from typing import Optional

from sqlalchemy import select

from .base import SQLAlchemyRepository, IRepository
from ..core.entities import App


class AppRepository(IRepository[App], ABC):
    @abstractmethod
    async def get_by_name(self, app_name: str) -> Optional[App]:
        raise NotImplementedError


class SQLAlchemyAppRepository(SQLAlchemyRepository[App], AppRepository):
    @staticmethod
    def _get_model():
        return App

    async def get_by_name(self, app_name: str) -> Optional[App]:
        statement = select(App).where(App.name == app_name)
        result = await self._session.execute(statement)
        return result.scalars().first()
