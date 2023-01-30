from datetime import datetime
from typing import List

from attrs import define, field

from core.interfaces.unit_of_work import UnitOfWork
from core.models.prices import PriceRecurring, PriceTier, Price


@define(kw_only=True, slots=False)
class CreatePriceCommand:
    product_id: str = field()
    recurring: PriceRecurring
    tiers: List[PriceTier]
    tiers_mode: str = field(default="graduated")


@define(kw_only=True, slots=False)
class CreatePriceResponse:
    id: str = field()
    product_id: str = field()
    created_at: datetime = field()
    active: bool = field()
    recurring: PriceRecurring
    tiers: List[PriceTier]
    tiers_mode: str = field(default="graduated")


class CreatePriceUseCase:
    def __init__(self, unit_of_work: UnitOfWork):
        self.unit_of_work = unit_of_work

    async def execute(self, command: CreatePriceCommand) -> CreatePriceResponse:
        async with self.unit_of_work:
            price_id = await self.unit_of_work.price_repository.next_id()
            price = Price(
                id=price_id,
                product_id=command.product_id,
                recurring=command.recurring,
                tiers=command.tiers,
                tiers_mode=command.tiers_mode,
            )
            await self.unit_of_work.price_repository.add(price)
            await self.unit_of_work.commit()

        return CreatePriceResponse(
            id=price.id,
            product_id=price.product_id,
            created_at=price.created_at,
            active=price.active,
            recurring=price.recurring,
            tiers=price.tiers,
            tiers_mode=price.tiers_mode,
        )
