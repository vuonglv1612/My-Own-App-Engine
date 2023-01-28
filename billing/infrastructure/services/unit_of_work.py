from abc import ABC, abstractmethod

from core.interfaces.repositories import AccountRepository, AccountBalanceRepository


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
