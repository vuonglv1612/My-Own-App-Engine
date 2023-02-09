from abc import abstractmethod, ABC
from typing import Optional, TypeVar, Generic

from core.models.accounts import Account, AccountBalance
from core.models.prices import Price
from core.models.products import Product
from core.models.invoice import Invoice
from core.models.accounts import Transaction
from core.models.subscriptions import Subscription, SubscriptionItem


T = TypeVar("T")


class Repository(ABC, Generic[T]):
    @abstractmethod
    async def next_id(self) -> str:
        """
        Returns the next id for the repository.
        """

    @abstractmethod
    async def add(self, entity: T) -> None:
        """
        Adds the entity to the repository.
        """

    @abstractmethod
    async def get(self, entity_id: str) -> Optional[T]:
        """
        Returns the entity with the given id.
        """


class AccountRepository(Repository[Account], ABC):
    pass


class AccountBalanceRepository(Repository[AccountBalance], ABC):
    @abstractmethod
    async def get_by_account_id(self, account_id: str) -> Optional[AccountBalance]:
        """
        Returns the account balance for the given account id.
        """


class ProductRepository(Repository[Product], ABC):
    pass


class PriceRepository(Repository[Price], ABC):
    pass


class SubscriptionRepository(Repository[Subscription], ABC):
    pass

class SubscriptionItemRepository(Repository[SubscriptionItem], ABC):
    pass


class TransactionRepository(Repository[Transaction], ABC):

    @abstractmethod
    async def list_transaction(self, account_id: str, page: int, page_size: int) -> Optional[Transaction]:
        pass

class InvoiceRepository(Repository[Invoice], ABC):

    @abstractmethod
    async def get_by_status(self, account_id, status: str, page: int, page_size: int) -> Optional[Invoice]:
        ...
