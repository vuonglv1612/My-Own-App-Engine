from abc import abstractmethod, ABC
from typing import Optional

from core.models.accounts import Account, AccountBalance


class AccountRepository(ABC):
    @abstractmethod
    async def add(self, account: Account) -> None:
        pass

    @abstractmethod
    async def get(self, account_id: str) -> Optional[Account]:
        pass


class AccountBalanceRepository(ABC):
    @abstractmethod
    async def add(self, account_balance: AccountBalance) -> None:
        pass

    @abstractmethod
    async def get(self, account_id: str) -> Optional[AccountBalance]:
        pass
