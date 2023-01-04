from abc import ABC
from typing import Optional

from sqlalchemy import select

from .base import SQLAlchemyRepository, IRepository
from ..core.entities import Plan


class PlanRepository(IRepository[Plan], ABC):
    async def get_current_plan(self) -> Optional[Plan]:
        raise NotImplementedError


class SQLAlchemyPlanRepository(SQLAlchemyRepository, PlanRepository):
    @staticmethod
    def _get_model():
        return Plan

    async def get_current_plan(self) -> Optional[Plan]:
        statement = select(Plan).where(Plan.active.is_(True))
        result = await self._session.execute(statement)
        return result.scalars().first()
