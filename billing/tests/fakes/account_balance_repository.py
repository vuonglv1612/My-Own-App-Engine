from core.interfaces.repositories import AccountBalanceRepository


class FakeAccountBalanceRepository(AccountBalanceRepository):
    def __init__(self):
        self._account_balances = {}

    async def get(self, account_id):
        return self._account_balances[account_id]

    async def add(self, account_balance):
        self._account_balances[account_balance.account_id] = account_balance
