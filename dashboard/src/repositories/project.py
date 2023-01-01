from abc import ABC

from .base import SQLAlchemyRepository, IRepository


class ProjectRepository(IRepository, ABC):
    pass


class SQLAlchemyProjectRepository(SQLAlchemyRepository, ProjectRepository):
    pass
