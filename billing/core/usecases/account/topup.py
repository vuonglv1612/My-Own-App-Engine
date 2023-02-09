from datetime import datetime
from typing import Optional

from attrs import define, field

from core.interfaces.unit_of_work import UnitOfWork
from core.models import Transaction


@define(kw_only=True, slots=False)
class TopupCommand:
    account_id: str = field()
    amount: float = field()
    type: str = field()
    description: str = field()


class TopupUseCase:
    def __init__(self, unit_of_work: UnitOfWork):
        self._uow = unit_of_work

    async def handle(self, command: TopupCommand):
        async with self._uow:
            transaction = Transaction(
                account_id=command.account_id,
                transaction_type=command.type,
                description=command.description,
                amount=command.amount
            )
            account_balance = await self._uow.account_balance_repository.get_by_account_id(command.account_id)
            account_balance.amount += command.amount
            await self._uow.account_balance_repository.add(account_balance)
            await self._uow.transaction_repository.add(transaction)
            await self._uow.commit()
            return transaction
