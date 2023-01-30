from datetime import datetime
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from api.dependencies import unit_of_work
from core.errors.prices import InvalidPriceTiersError, InvalidPriceTiersModeError
from core.interfaces.unit_of_work import UnitOfWork
from core.usecases.price.create_price import CreatePriceUseCase, CreatePriceCommand, PriceTier, PriceRecurring

router = APIRouter()


class PriceTierBody(BaseModel):
    unit_amount: float = Field(..., example=1000, description="The unit amount of the price tier")
    flat_amount: float = Field(..., example=0, description="The flat amount of the price tier")
    up_to: int | str = Field(..., example=1000,
                             description="The number of units this tier applies to, or 'inf' for infinity")


class PriceRecurringBody(BaseModel):
    interval: str = Field(..., example="month", description="The interval of the recurring price")
    interval_count: int = Field(..., example=1, description="The number of intervals between each recurring price")
    aggregate_usage: str = Field(..., example="sum",
                                 description="The aggregate usage of the recurring price, supported sum")


class CreatePriceBody(BaseModel):
    product_id: str = Field(..., example="product_id")
    recurring: PriceRecurringBody = Field(..., description="Recurring setting")
    tiers: List[PriceTierBody] = Field(..., min_items=1, description="List of price tiers")
    tiers_mode: str = Field(..., description="one of 'graduated', 'volume'")


class CreatePriceResponse(BaseModel):
    id: str = Field(..., example="price_id")
    created_at: datetime = Field(..., example="2021-01-01T00:00:00Z")
    active: bool = Field(..., example=True)
    product_id: str = Field(..., example="product_id")
    recurring: PriceRecurringBody = Field(..., description="Recurring setting")
    tiers: List[PriceTierBody] = Field(..., min_items=1, description="List of price tiers")
    tiers_mode: str = Field(..., description="one of 'graduated', 'volume'", example="graduated")


@router.post("", response_model=CreatePriceResponse)
async def create_price(body: CreatePriceBody, uow: UnitOfWork = Depends(unit_of_work)):
    use_case = CreatePriceUseCase(uow)
    recurring = PriceRecurring(
        interval=body.recurring.interval,
        interval_count=body.recurring.interval_count,
        aggregate_usage=body.recurring.aggregate_usage,
    )
    tiers = [PriceTier(**tier.dict()) for tier in body.tiers]
    command = CreatePriceCommand(
        product_id=body.product_id,
        recurring=recurring,
        tiers=tiers,
        tiers_mode=body.tiers_mode,
    )
    try:
        response = await use_case.execute(command)
    except (InvalidPriceTiersError, InvalidPriceTiersModeError) as e:
        raise HTTPException(status_code=400, detail=str(e))
    return CreatePriceResponse(
        id=response.id,
        created_at=response.created_at,
        active=response.active,
        product_id=response.product_id,
        recurring=PriceRecurringBody(
            interval=response.recurring.interval,
            interval_count=response.recurring.interval_count,
            aggregate_usage=response.recurring.aggregate_usage,
        ),
        tiers=[PriceTierBody(unit_amount=tier.unit_amount, flat_amount=tier.flat_amount, up_to=tier.up_to) for tier in
               response.tiers],
        tiers_mode=response.tiers_mode,
    )
