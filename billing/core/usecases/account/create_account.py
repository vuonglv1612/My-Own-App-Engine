import uuid

from attrs import define, field

from core.models.accounts import Account, AccountBalance
from ...interfaces.repositories import AccountRepository, AccountBalanceRepository


@define(kw_only=True, slots=False)
class CreateAccountCommand:
    name: str = field(default=None)
    address: str = field(default=None)
    description: str = field(default=None)
    email: str = field(default=None)
    phone: str = field(default=None)


@define(kw_only=True, slots=False)
class CreateAccountResponse:
    id: str = field()
    balance: float = field()
    name: str = field(default=None)
    address: str = field(default=None)
    description: str = field(default=None)
    email: str = field(default=None)
    phone: str = field(default=None)


class CreateAccountUseCase:
    def __init__(self, account_repository: AccountRepository, account_balance_repository: AccountBalanceRepository):
        self._account_repository = account_repository
        self._account_balance_repository = account_balance_repository

    async def handle(self, command: CreateAccountCommand):
        account_id = str(uuid.uuid4())
        account = Account(
            id=account_id,
            name=command.name,
            address=command.address,
            description=command.description,
            email=command.email,
            phone=command.phone,
        )
        account_balance = AccountBalance(account_id=account_id)
        await self._account_repository.add(account)
        await self._account_balance_repository.add(account_balance)

        response = CreateAccountResponse(
            id=account.id,
            balance=account_balance.amount,
            name=account.name,
            address=account.address,
            description=account.description,
            email=account.email,
            phone=account.phone,
        )
        return response
