from core.interfaces.unit_of_work import UnitOfWork
from ..repositories_adapters.sqlalchemy_account_balance_repo import SqlalchemyAccountBalanceRepository
from ..repositories_adapters.sqlalchemy_account_repo import SqlalchemyAccountRepository
from ..repositories_adapters.sqlalchemy_price_repo import SqlalchemyPriceRepository
from ..repositories_adapters.sqlalchemy_product_repo import SqlalchemyProductRepository


class SqlalchemyUnitOfWork(UnitOfWork):
    def __init__(self, session_factory):
        self._session_factory = session_factory

    async def __aenter__(self):
        self.session = self._session_factory()
        self.account_repository = SqlalchemyAccountRepository(self.session)
        self.account_balance_repository = SqlalchemyAccountBalanceRepository(self.session)
        self.product_repository = SqlalchemyProductRepository(self.session)
        self.price_repository = SqlalchemyPriceRepository(self.session)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await super().__aexit__(exc_type, exc_val, exc_tb)
        await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()
