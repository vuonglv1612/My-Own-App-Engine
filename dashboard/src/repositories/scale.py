from abc import ABC, abstractmethod
from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from .base import SQLAlchemyRepository, IRepository
from ..core.entities import Scale


class ScaleRepository(IRepository[Scale], ABC):
    """
    Scale repository interface.
    """

    @abstractmethod
    async def get_active_by_app_id(self, app_id: str) -> Optional[Scale]:
        raise NotImplementedError

    async def list_by_app_id(self, app_id: str):
        raise NotImplementedError


class SQLAlchemyScaleRepository(SQLAlchemyRepository[Scale], ScaleRepository):

    @staticmethod
    def _get_model():
        return Scale

    async def get_active_by_app_id(self, app_id: str) -> Optional[Scale]:
        statement = select(Scale).where(Scale.app_id == app_id, Scale.active == True)
        statement = statement.options(selectinload(Scale.unit))
        result = await self._session.execute(statement)
        return result.scalars().first()

    async def list_by_app_id(self, app_id: str):
        statement = select(Scale).where(Scale.app_id == app_id).order_by(Scale.created_at.desc())
        result = await self._session.execute(statement)
        return result.scalars().all()
