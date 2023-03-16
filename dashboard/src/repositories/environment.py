from abc import ABC

from sqlalchemy import select, func

from .base import SQLAlchemyRepository, IRepository
from ..core.entities import Environment


class EnvironmentRepository(IRepository[Environment], ABC):
    """
    Environment repository interface.
    """

    async def list_app_environments(self, app_id: str, page: int, page_size: int) -> list[Environment]:
        """
        List all environments of an app.
        """
        raise NotImplementedError

    async def get_by_name(self, name: str) -> Environment:
        """
        Get an environment by name.
        """
        raise NotImplementedError

    async def delete(self, entity: Environment) -> None:
        """
        Delete an environment.
        """
        raise NotImplementedError

    async def create(self, name, value, app_id):
        raise NotImplementedError


class SQLAlchemyEnvironmentRepository(SQLAlchemyRepository[Environment], EnvironmentRepository):
    async def get_by_name(self, name: str) -> Environment:
        query = select(Environment).where(Environment.name == name)
        result = await self._session.execute(query)
        return result.scalars().first()

    async def delete(self, entity: Environment) -> None:
        await self._session.delete(entity)

    async def list_app_environments(self, app_id: str, page: int, page_size: int):
        count_query = select(func.count(Environment.id)).where(Environment.app_id == app_id)
        total = (await self._session.execute(count_query)).scalar()
        query = select(Environment).where(Environment.app_id == app_id)
        query = query.offset((page - 1) * page_size).limit(page_size)
        result = await self._session.execute(query)
        return result.scalars().all(), total

    async def create(self, name, value, app):
        env = Environment(name=name, value=value, app_id=app.id)
        env.app = app
        self._session.add(env)
        return env

    @staticmethod
    def _get_model():
        return Environment
