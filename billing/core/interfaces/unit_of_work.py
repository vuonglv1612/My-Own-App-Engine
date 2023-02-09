from abc import ABC, abstractmethod

from .repositories import TransactionRepository, InvoiceRepository, AccountRepository, AccountBalanceRepository, ProductRepository, PriceRepository, SubscriptionRepository, SubscriptionItemRepository

class UnitOfWork(ABC):
    account_repository: AccountRepository
    account_balance_repository: AccountBalanceRepository
    product_repository: ProductRepository
    price_repository: PriceRepository
    subscription_repository: SubscriptionRepository
    subscription_item_repository: SubscriptionItemRepository
    invoice_repository: InvoiceRepository
    transaction_repository: TransactionRepository

    @abstractmethod
    async def __aenter__(self):
        """
        Starts the unit of work.
        We use this method to start a transaction and initialize the repositories.
        """

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.rollback()

    @abstractmethod
    async def commit(self):
        """
        Commits the unit of work.
        :return: None
        """

    @abstractmethod
    async def rollback(self):
        """
        Rolls back the unit of work.
        :return:
        """
