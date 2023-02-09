from datetime import datetime, timedelta
from typing import List, Optional

from attrs import define, field
from utils.datetime import aware_now

from core.interfaces.unit_of_work import UnitOfWork
from core.models import Invoice, InvoiceLine


@define(kw_only=True, slots=False)
class GetInvoicesCommand:
    account_id: str = field()
    status: Optional[str] = field()
    page: int = field()
    page_size: int = field()


@define(kw_only=True, slots=False)
class InvoiceResponse:
    id: str = field()
    created_at: datetime = field(factory=aware_now)
    deleted_at: datetime = field(factory=aware_now)
    sub_id: str = field()
    due: datetime = field(factory=lambda: aware_now() + timedelta(days=3))
    status: str = field(default="open")
    account_id: str = field()
    account_address: str = field(default=None)
    account_email: str = field(default=None)
    amount: float = field()
    period_start: int = field()
    period_end: int = field()
    #lines: List[InvoiceLine]


class GetInvoicesUseCase:
    def __init__(self, unit_of_work: UnitOfWork):
        self._uow = unit_of_work

    async def handle(self, command: GetInvoicesCommand) -> List[InvoiceResponse]:
        async with self._uow:
            invoices = await self._uow.invoice_repository.get_by_status(command.account_id, command.status, command.page, command.page_size)
            response = []
            for invoice, in invoices:
                response.append(InvoiceResponse(
                    id=invoice.id,
                    created_at=invoice.created_at,
                    deleted_at=invoice.deleted_at,
                    sub_id=invoice.sub_id,
                    due=invoice.due,
                    status=invoice.status,
                    account_id=invoice.account_id,
                    account_address=invoice.account_address,
                    account_email=invoice.account_email,
                    amount=invoice.amount,
                    period_end=invoice.period_end,
                    period_start=invoice.period_start
                ))
            return response
