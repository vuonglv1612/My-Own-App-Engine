from src.services.unit_of_work import UnitOfWork
from .fake_app_repository import MemoryAppRepository


class MemoryUnitOfWork(UnitOfWork):
    def __init__(self):
        self.committed = False

    async def _connect(self):
        self.apps = MemoryAppRepository()

    async def _disconnect(self):
        pass

    async def rollback(self):
        pass

    async def commit(self):
        self.committed = True
