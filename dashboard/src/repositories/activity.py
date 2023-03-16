from abc import ABC, abstractmethod

from sqlalchemy import select, func
from sqlalchemy.orm import selectinload

from .base import SQLAlchemyRepository, IRepository
from ..core.entities import Activity


class ActivityRepository(IRepository[Activity], ABC):
    """
    Activity repository interface.
    """

    @abstractmethod
    async def list_app_activity(self, app_id: str, page: int, page_size: int):
        raise NotImplementedError


class SQLAlchemyActivityRepository(SQLAlchemyRepository[Activity], ActivityRepository):
    async def list_app_activity(self, app_id: str, page: int, page_size: int):
        count_query = select(func.count(self._model.id)).where(
            self._model.app_id == app_id)
        total = (await self._session.execute(count_query)).scalar()
        query = select(self._model).where(self._model.app_id == app_id)
        offset = (page - 1) * page_size
        query = query.offset(offset).limit(page_size).options(
            selectinload(self._model.app))
        result = await self._session.execute(query)
        return result.scalars().all(), total

    @staticmethod
    def _get_model():
        return Activity
