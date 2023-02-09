from datetime import datetime
from typing import Optional

from attrs import asdict
from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field

from api.dependencies import unit_of_work
from core.interfaces.unit_of_work import UnitOfWork
from core.usecases.account.get_transaction import GetTransactionCommand, GetTransactionUseCase

router = APIRouter()


class GetTransaction(BaseModel):
    account_id: str
    page: int = 1
    page_size: int = 50


@router.get("")
async def get_transactions(body: GetTransaction = Depends(), uow: UnitOfWork = Depends(unit_of_work)):
    command = GetTransactionCommand(
        account_id=body.account_id,
        page=body.page,
        page_size=body.page_size
    )
    handler = GetTransactionUseCase(uow)
    response = await handler.handle(command)
    return response
