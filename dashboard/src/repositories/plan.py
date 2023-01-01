from abc import ABC

from .base import SQLAlchemyRepository, IRepository


class PlanRepository(IRepository, ABC):
    pass


class SQLAlchemyPlanRepository(SQLAlchemyRepository, PlanRepository):
    pass
