from abc import ABC, abstractmethod

from sqlalchemy import select

from .base import SQLAlchemyRepository, IRepository
from ..core.entities import Unit


class UnitRepository(IRepository[Unit], ABC):
    """
    Unit repository interface.
    """

    @abstractmethod
    async def get_all(self, active: bool = True):
        pass


class SQLAlchemyUnitRepository(SQLAlchemyRepository[Unit], UnitRepository):
    @staticmethod
    def _get_model():
        return Unit

    async def get_all(self, active: bool = True):
        statement = select(Unit).where(Unit.active == active)
        result = await self._session.execute(statement)
        return result.scalars().all()
