from abc import ABC, abstractmethod
from typing import Optional, Generic, TypeVar

T = TypeVar("T")


class IRepository(ABC, Generic[T]):
    @abstractmethod
    async def get(self, entity_id: str) -> Optional[T]:
        pass

    @abstractmethod
    async def add(self, entity: T) -> None:
        pass


class SQLAlchemyRepository(IRepository, Generic[T]):
    def __init__(self, session):
        self._session = session

    async def get(self, entity_id: str) -> Optional[T]:
        result = await self._session.get(entity_id)
        if not result:
            return None
        return result

    async def add(self, entity: T) -> None:
        self._session.add(entity)
