from abc import ABC, abstractmethod

from src.repositories.app import AppRepository, SQLAlchemyAppRepository, MemoryAppRepository


class UnitOfWork(ABC):
    apps: AppRepository

    async def __aenter__(self):
        await self._connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.rollback()
        await self._disconnect()

    @abstractmethod
    async def _connect(self):
        pass

    @abstractmethod
    async def _disconnect(self):
        pass

    @abstractmethod
    async def rollback(self):
        pass

    @abstractmethod
    async def commit(self):
        pass


class MemoryUnitOfWork(UnitOfWork):
    async def _connect(self):
        self.apps = MemoryAppRepository()

    async def _disconnect(self):
        pass

    async def rollback(self):
        pass

    async def commit(self):
        pass


class SQLAlchemyUnitOfWork(UnitOfWork):
    def __init__(self, session_factory):
        self._session_factory = session_factory

    async def _connect(self):
        self._session = self._session_factory()
        self.apps = SQLAlchemyAppRepository(self._session)

    async def _disconnect(self):
        await self._session.close()

    async def rollback(self):
        await self._session.rollback()

    async def commit(self):
        await self._session.commit()
