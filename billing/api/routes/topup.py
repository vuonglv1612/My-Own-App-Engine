from datetime import datetime
from typing import Optional

from attrs import asdict
from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field

from api.dependencies import unit_of_work
from core.interfaces.unit_of_work import UnitOfWork
from core.usecases.account.topup import TopupCommand, TopupUseCase

router = APIRouter()


class TopupBody(BaseModel):
    account_id: str
    amount: float
    description: str


@router.post("")
async def top_up(body: TopupBody, uow: UnitOfWork = Depends(unit_of_work)):
    command = TopupCommand(
        account_id=body.account_id,
        amount=body.amount,
        type="topup",
        description=body.description,
    )
    handler = TopupUseCase(uow)
    response = await handler.handle(command)
    return asdict(response)
