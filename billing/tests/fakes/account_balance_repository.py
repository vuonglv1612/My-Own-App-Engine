import uuid
from typing import Optional

from core.interfaces.repositories import AccountBalanceRepository
from core.models import AccountBalance


class FakeAccountBalanceRepository(AccountBalanceRepository):
    async def next_id(self) -> str:
        return str(uuid.uuid4().hex)

    def __init__(self):
        self._account_balances = {}

    async def get(self, account_id):
        return self._account_balances[account_id]

    async def add(self, account_balance):
        self._account_balances[account_balance.id] = account_balance

    async def get_by_account_id(self, account_id: str) -> Optional[AccountBalance]:
        for account_balance in self._account_balances.values():
            if account_balance.account_id == account_id:
                return account_balance
        return None
