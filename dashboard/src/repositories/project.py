from abc import ABC
from typing import Optional

from sqlalchemy import select, func
from sqlalchemy.orm import selectinload

from .base import SQLAlchemyRepository, IRepository
from ..core.entities import Project, ProjectMember


class ProjectRepository(IRepository[Project], ABC):
    async def list_by_user(self, user_id: str, page: int, per_page: int):
        raise NotImplementedError

    async def remove_member(self, project_id: str, user_id: str):
        raise NotImplementedError

    async def list_members(self, project_id: str, page: int, page_size: int):
        raise NotImplementedError

    async def add_member(self, project, user, role: str):
        raise NotImplementedError

    async def delete(self, project):
        raise NotImplementedError


class SQLAlchemyProjectRepository(SQLAlchemyRepository, ProjectRepository):
    async def get_by_id(self, entity_id: str) -> Optional[Project]:
        query = select(self._model).where(self._model.id == entity_id)
        query = query.options(selectinload(Project.members))
        result = await self._session.execute(query)
        return result.scalars().first()

    async def list_by_user(self, user_id: str, page: int, per_page: int):
        query = select(func.count(Project.id)).join(ProjectMember).filter(ProjectMember.user_id == user_id)
        total = (await self._session.execute(query)).scalar()
        query = select(Project, ProjectMember).join(ProjectMember).filter(ProjectMember.user_id == user_id)
        offset = (page - 1) * per_page
        query = query.offset(offset).limit(per_page)
        result = await self._session.execute(query)
        projects = []
        for project, project_member in result.all():
            data = {"id": project.id, "name": project.name, "account_id": project.account_id,
                    "created_at": project.created_at, "deleted_at": project.deleted_at, "deleted": project.deleted,
                    "suspended": project.suspended, "role": project_member.role}
            projects.append(data)
        return total, projects

    async def remove_member(self, project_id: str, user_id: str):
        query = select(ProjectMember).where(ProjectMember.project_id == project_id, ProjectMember.user_id == user_id)
        result = await self._session.execute(query)
        project_member = result.scalars().first()
        if project_member:
            await self._session.delete(project_member)
        return project_member

    async def list_members(self, project_id: str, page: int, page_size: int):
        query = select(func.count(ProjectMember.id)).where(ProjectMember.project_id == project_id)
        total = (await self._session.execute(query)).scalar()
        query = select(ProjectMember).where(ProjectMember.project_id == project_id).options(
            selectinload(ProjectMember.user))
        offset = (page - 1) * page_size
        query = query.offset(offset).limit(page_size)
        result = await self._session.execute(query)
        members = result.scalars().all()
        return members, total

    async def add_member(self, project, user, role: str):
        project_member = ProjectMember(project_id=project.id, user_id=user.id, role=role)
        self._session.add(project_member)
        return project_member

    async def delete(self, project: str):
        await self._session.delete(project)

    @staticmethod
    def _get_model():
        return Project
