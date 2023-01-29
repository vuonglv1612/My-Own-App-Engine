from infrastructure.services.unit_of_work import UnitOfWork
from .account_balance_repository import FakeAccountBalanceRepository
from .account_repository import FakeAccountRepository


class FakeUnitOfWork(UnitOfWork):
    async def __aenter__(self):
        self.account_repository = FakeAccountRepository()
        self.account_balance_repository = FakeAccountBalanceRepository()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pass

    async def commit(self):
        pass

    async def rollback(self):
        pass


class UnitOfWorkFactory:
    @staticmethod
    def for_create_account():
        return FakeUnitOfWork()
