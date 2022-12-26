from abc import ABC

from .base import SQLAlchemyRepository, IRepository


class AppRepository(IRepository, ABC):
    pass


class SQLAlchemyAppRepository(SQLAlchemyRepository, AppRepository):
    pass
