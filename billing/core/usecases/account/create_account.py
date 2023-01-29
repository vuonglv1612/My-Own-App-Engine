from datetime import datetime

from attrs import define, field

from core.models.accounts import Account, AccountBalance
from ...interfaces.unit_of_work import UnitOfWork


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
    created_at: datetime = field()
    balance: float = field()
    name: str = field(default=None)
    address: str = field(default=None)
    description: str = field(default=None)
    email: str = field(default=None)
    phone: str = field(default=None)


class CreateAccountUseCase:
    def __init__(self, unit_of_work: UnitOfWork):
        self._uow = unit_of_work

    async def handle(self, command: CreateAccountCommand) -> CreateAccountResponse:
        async with self._uow:
            account_id = await self._uow.account_repository.next_id()
            account = Account(
                id=account_id,
                name=command.name,
                address=command.address,
                description=command.description,
                email=command.email,
                phone=command.phone,
            )
            account_balance_id = await self._uow.account_balance_repository.next_id()
            account_balance = AccountBalance(
                id=account_balance_id,
                account_id=account_id,
                amount=0.0,
            )
            await self._uow.account_repository.add(account)
            await self._uow.account_balance_repository.add(account_balance)
            await self._uow.commit()
            return CreateAccountResponse(
                id=account_id,
                created_at=account.created_at,
                balance=account_balance.amount,
                name=account.name,
                address=account.address,
                description=account.description,
                email=account.email,
                phone=account.phone,
            )
