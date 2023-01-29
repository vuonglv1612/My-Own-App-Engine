from abc import abstractmethod, ABC
from typing import Optional, TypeVar, Generic

from core.models.accounts import Account, AccountBalance

T = TypeVar("T")


class Repository(ABC, Generic[T]):
    @abstractmethod
    async def add(self, entity: T) -> None:
        pass

    @abstractmethod
    async def get(self, entity_id: str) -> Optional[T]:
        pass


class AccountRepository(Repository[Account], ABC):
    pass


class AccountBalanceRepository(Repository[AccountBalance], ABC):
    @abstractmethod
    async def get_by_account_id(self, account_id: str) -> Optional[AccountBalance]:
        pass
