from abc import ABC, abstractmethod
from typing import Optional, TypeVar, Type
from uuid import uuid4

from sqlalchemy import select

from core.interfaces.repositories import Repository

T = TypeVar("T")


class SqlalchemyRepository(Repository[T], ABC):
    def __init__(self, session):
        self._session = session

    @property
    @abstractmethod
    def entity(self) -> Type[T]:
        pass

    async def next_id(self) -> str:
        return str(uuid4().hex)

    async def add(self, entity: T) -> None:
        self._session.add(entity)

    async def get(self, entity_id: str) -> Optional[T]:
        query = select(self.entity).where(self.entity.id == entity_id)
        result = await self._session.execute(query)
        return result.scalars().first()
