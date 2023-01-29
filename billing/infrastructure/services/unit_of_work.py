from abc import ABC, abstractmethod

from core.interfaces.repositories import AccountRepository, AccountBalanceRepository
from ..repositories_adapters.sqlalchemy_account_balance_repo import SqlalchemyAccountBalanceRepository
from ..repositories_adapters.sqlalchemy_account_repo import SqlalchemyAccountRepository


class UnitOfWork(ABC):
    account_repository: AccountRepository
    account_balance_repository: AccountBalanceRepository

    @abstractmethod
    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.rollback()

    @abstractmethod
    async def commit(self):
        pass

    @abstractmethod
    async def rollback(self):
        pass


class SqlalchemyUnitOfWork(UnitOfWork):
    def __init__(self, session_factory):
        self._session_factory = session_factory

    async def __aenter__(self):
        self.session = self._session_factory()
        self.account_repository = SqlalchemyAccountRepository(self.session)
        self.account_balance_repository = SqlalchemyAccountBalanceRepository(self.session)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await super().__aexit__(exc_type, exc_val, exc_tb)
        await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()
