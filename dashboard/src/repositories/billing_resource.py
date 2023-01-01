from abc import ABC

from .base import SQLAlchemyRepository, IRepository


class BillingResourceRepository(IRepository, ABC):
    pass


class SQLAlchemyBillingResourceRepository(SQLAlchemyRepository, BillingResourceRepository):
    pass
