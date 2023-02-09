from datetime import datetime
from typing import List, Optional

from attrs import asdict
from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field

from api.dependencies import unit_of_work
from core.interfaces.unit_of_work import UnitOfWork
from core.usecases.subscription.create_subscription import CreateSubscriptionCommand, CreateSubscriptionUseCase, Item
from core.usecases.subscription.delete_subscription import DeleteSubscriptionCommand, DeleteSubscriptionUseCase
router = APIRouter()


class ItemBody(BaseModel):
    price_id: str


class CreateSubscriptionBody(BaseModel):
    account_id: str
    items: List[ItemBody]


class ItemResponse(BaseModel):
    item_id: str
    sub_id: str
    price_id: str
    quantity: int


class CreateSubscriptionResponse(BaseModel):
    sub_id: str
    account_id: str
    current_period_start: int
    current_period_end: int
    cancel_at: int = None
    cancelled: bool
    status: str
    items: List[ItemResponse]


@router.post("", response_model=CreateSubscriptionResponse)
async def create_subscription(body: CreateSubscriptionBody, uow: UnitOfWork = Depends(unit_of_work)):
    """
    Create a new subscription
    """
    items = []
    for item in body.items:
        items.append(Item(
            price_id=item.price_id,
        ))
    command = CreateSubscriptionCommand(
        account_id=body.account_id,
        items=items,
    )
    handler = CreateSubscriptionUseCase(uow)
    response = await handler.handle(command)
    return asdict(response)


@router.delete("/{sub_id}")
async def delete_subscription(sub_id: str, uow: UnitOfWork = Depends(unit_of_work)):
    command = DeleteSubscriptionCommand(
        sub_id=sub_id
    )
    handler = DeleteSubscriptionUseCase(uow)
    response = await handler.handle(command)
    return asdict(response)
