from datetime import datetime
from typing import Optional

from attrs import asdict
from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field

from api.dependencies import unit_of_work
from core.interfaces.unit_of_work import UnitOfWork
from core.usecases.invoice.get_invoice import GetInvoicesCommand, GetInvoicesUseCase

router = APIRouter()


class GetInvoice(BaseModel):
    status: Optional[str] = None
    account_id: str
    page: int = 1
    page_size: int = 50


@router.get("")
async def get_invoices(body: GetInvoice = Depends(), uow: UnitOfWork = Depends(unit_of_work)):
    command = GetInvoicesCommand(
        account_id=body.account_id,
        status=body.status,
        page=body.page,
        page_size=body.page_size
    )
    handler = GetInvoicesUseCase(uow)
    response = await handler.handle(command)
    return response
