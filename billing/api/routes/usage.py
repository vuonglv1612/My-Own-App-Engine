from datetime import datetime
from typing import Optional

from attrs import asdict
from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field

from api.dependencies import unit_of_work, create_invoice
from core.interfaces.unit_of_work import UnitOfWork
from core.usecases.usage.report_usage import ReportUsageCommand, ReportUsageUseCase

router = APIRouter()


class ReportUsageBody(BaseModel):
    subscription_item_id: str
    timestamp: int
    quantity: int


@router.post("")
async def report_usage(body: ReportUsageBody, uow: UnitOfWork = Depends(unit_of_work)):
    command = ReportUsageCommand(
        subscription_item_id=body.subscription_item_id,
        timestamp=body.timestamp,
        quantity=body.quantity
    )
    handler = ReportUsageUseCase(uow, create_invoice)
    response = await handler.handle(command)
    return response
