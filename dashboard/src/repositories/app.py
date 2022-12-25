from abc import ABC

from .base import SQLAlchemyRepository, IRepository


class AppRepository(IRepository, ABC):
    pass


class MemoryAppRepository(AppRepository):
    def __init__(self):
        self._data = {}

    async def get(self, entity_id: str):
        return self._data.get(entity_id)

    async def add(self, entity):
        self._data[entity.id] = entity


class SQLAlchemyAppRepository(SQLAlchemyRepository, AppRepository):
    pass
