from core.interfaces.repositories import AccountRepository, AccountBalanceRepository
from .account_balance_repository import FakeAccountBalanceRepository
from .account_repository import FakeAccountRepository


class UnitOfWork(object):
    """Fake unit of work for testing."""
    account_repository: AccountRepository
    account_balance_repository: AccountBalanceRepository

    def __init__(self):
        self.committed = False

    def __enter__(self):
        self.account_repository = FakeAccountRepository()
        self.account_balance_repository = FakeAccountBalanceRepository()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.rollback()

    def commit(self):
        self.committed = True

    def rollback(self):
        pass


class UnitOfWorkFactory:
    @staticmethod
    def for_create_account():
        return UnitOfWork()
