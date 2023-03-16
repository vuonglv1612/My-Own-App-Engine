from abc import ABC

from sqlalchemy import select

from .base import SQLAlchemyRepository, IRepository
from ..core.entities.users import User


class UserRepository(IRepository[User], ABC):
    async def get_by_email(self, email: str) -> User:
        raise NotImplementedError


class SQLAlchemyUserRepository(UserRepository, SQLAlchemyRepository[User]):
    @staticmethod
    def _get_model():
        return User

    async def get_by_email(self, email: str) -> User:
        query = select(self._get_model()).where(self._get_model().email == email)
        result = await self._session.execute(query)
        return result.scalars().first()
