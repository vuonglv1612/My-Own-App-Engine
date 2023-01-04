from abc import ABC, abstractmethod
from typing import Optional, Generic, TypeVar

from sqlalchemy import select

T = TypeVar("T")


class IRepository(ABC, Generic[T]):
    @abstractmethod
    async def get_by_id(self, entity_id: str) -> Optional[T]:
        pass

    @abstractmethod
    async def add(self, entity: T) -> None:
        pass


class SQLAlchemyRepository(IRepository, ABC, Generic[T]):
    def __init__(self, session):
        self._session = session
        self._model = self._get_model()

    @staticmethod
    @abstractmethod
    def _get_model():
        raise NotImplementedError

    async def get_by_id(self, entity_id: str) -> Optional[T]:
        statement = select(self._model).where(self._model.id == entity_id)
        result = await self._session.execute(statement)
        return result.scalars().first()

    async def add(self, entity: T) -> None:
        self._session.add(entity)
