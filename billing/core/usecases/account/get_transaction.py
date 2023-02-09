from datetime import datetime, timedelta
from typing import List, Optional

from attrs import define, field
from utils.datetime import aware_now

from core.interfaces.unit_of_work import UnitOfWork
from core.models import Invoice, InvoiceLine


@define(kw_only=True, slots=False)
class GetTransactionCommand:
    account_id: str = field()
    page: int = field()
    page_size: int = field()


@define(kw_only=True, slots=False)
class TransactionResponse:
    id: str = field()
    created_at: datetime = field(factory=aware_now)
    account_id: str = field()
    amount: float = field()
    transaction_type: str = field()
    description: str = field(default=None)




class GetTransactionUseCase:
    def __init__(self, unit_of_work: UnitOfWork):
        self._uow = unit_of_work

    async def handle(self, command: GetTransactionCommand):
        async with self._uow:
            transactions = await self._uow.transaction_repository.list_transaction(command.account_id, command.page, command.page_size)
            responses = []
            for transaction, in transactions:
                responses.append(TransactionResponse(
                    id=transaction.id,
                    created_at=transaction.created_at,
                    account_id=transaction.account_id,
                    amount=transaction.amount,
                    transaction_type=transaction.transaction_type,
                    description=transaction.description
                ))
            return responses