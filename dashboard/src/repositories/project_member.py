from abc import ABC

from sqlalchemy import select

from .base import SQLAlchemyRepository, IRepository
from ..core.entities.project import ProjectMember


class ProjectMemberRepository(IRepository[ProjectMember], ABC):
    async def get_by_project_and_user(self, project_id: str, user_id: str):
        raise NotImplementedError


class SQLAlchemyProjectMemberRepository(ProjectMemberRepository, SQLAlchemyRepository[ProjectMember]):
    @staticmethod
    def _get_model():
        return ProjectMember

    async def get_by_project_and_user(self, project_id: str, user_id: str):
        query = select(self._model).where(self._model.project_id == project_id, self._model.user_id == user_id)
        result = await self._session.execute(query)
        return result.scalars().first()
