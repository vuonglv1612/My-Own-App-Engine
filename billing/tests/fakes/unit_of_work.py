from core.interfaces.unit_of_work import UnitOfWork
from .account_balance_repository import FakeAccountBalanceRepository
from .account_repository import FakeAccountRepository
from .product_repository import FakeProductRepository


class FakeUnitOfWork(UnitOfWork):
    def __init__(self):
        self.committed = False

    async def __aenter__(self):
        self.account_repository = FakeAccountRepository()
        self.account_balance_repository = FakeAccountBalanceRepository()
        self.product_repository = FakeProductRepository()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pass

    async def commit(self):
        self.committed = True

    async def rollback(self):
        pass


class UnitOfWorkFactory:
    @staticmethod
    def for_create_account():
        return FakeUnitOfWork()

    @staticmethod
    def for_create_product():
        return FakeUnitOfWork()
