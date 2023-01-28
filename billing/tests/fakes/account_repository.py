from core.interfaces.repositories import AccountRepository


class FakeAccountRepository(AccountRepository):
    def __init__(self):
        self._accounts = {}

    async def add(self, account):
        self._accounts[account.id] = account

    async def get(self, account_id):
        return self._accounts.get(account_id)
