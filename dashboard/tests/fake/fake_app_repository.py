from src.repositories.app import AppRepository


class MemoryAppRepository(AppRepository):
    def __init__(self):
        self._data = {}

    async def get_by_id(self, entity_id: str):
        return self._data.get(entity_id)

    async def add(self, entity):
        self._data[entity.id] = entity
