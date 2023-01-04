from abc import ABC

from .base import SQLAlchemyRepository, IRepository
from ..core.entities import Project


class ProjectRepository(IRepository[Project], ABC):
    pass


class SQLAlchemyProjectRepository(SQLAlchemyRepository, ProjectRepository):
    @staticmethod
    def _get_model():
        return Project
