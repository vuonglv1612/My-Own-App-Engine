from core.interfaces.unit_of_work import UnitOfWork
from .account_balance_repository import FakeAccountBalanceRepository
from .account_repository import FakeAccountRepository
from .price_repository import FakePriceRepository
from .product_repository import FakeProductRepository


class FakeUnitOfWork(UnitOfWork):
    def __init__(self):
        self.committed = False

    async def __aenter__(self):
        self.account_repository = FakeAccountRepository()
        self.account_balance_repository = FakeAccountBalanceRepository()
        self.product_repository = FakeProductRepository()
        self.price_repository = FakePriceRepository()
        return self

    async def commit(self):
        self.committed = True

    async def rollback(self):
        pass


class UnitOfWorkFactory:
    @staticmethod
    def new():
        return FakeUnitOfWork()

    @staticmethod
    def for_create_account():
        return FakeUnitOfWork()

    @staticmethod
    def for_create_product():
        return FakeUnitOfWork()
