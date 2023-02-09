from datetime import datetime
from typing import List, Optional
import uuid

from attrs import define, field

from core.interfaces.unit_of_work import UnitOfWork
from core.models import Subscription, SubscriptionItem
from core.errors import prices


@define(kw_only=True, slots=False)
class Item:
    price_id: str = field()


@define(kw_only=True, slots=False)
class ItemResponse:
    item_id: str = field()
    sub_id: str = field()
    price_id: str = field()
    quantity: int = field()


@define(kw_only=True, slots=False)
class CreateSubscriptionCommand:
    account_id: str = field()
    items: List[Item] = field(default=[])


@define(kw_only=True, slots=False)
class CreateSubscriptionResponse:
    sub_id: str = field()
    account_id: str = field()
    current_period_start: int = field()
    current_period_end: int = field()
    cancel_at: Optional[int] = field(default=None)
    cancelled: bool = field()
    status: str = field()
    items: List[ItemResponse]


interval_mapping = {
    "day": 86400,
    "week": 604800,
    "month": 2592000,
    "year": 31536000,
}


class CreateSubscriptionUseCase:

    def __init__(self, unit_of_work: UnitOfWork) -> None:
        self._uow = unit_of_work

    async def handle(self, command: CreateSubscriptionCommand) -> CreateSubscriptionResponse:
        async with self._uow:
            #happy case
            sub_id = uuid.uuid4().hex
            dt = datetime.now()
            item, = command.items
            price = await self._uow.price_repository.get(item.price_id)
            if not price:
                raise prices.PriceNotFoundError
            recurring = price.recurring
            interval_in_seconds = interval_mapping[recurring.interval] * recurring.interval_count
            current_period_start = datetime.timestamp(dt)
            current_period_end = current_period_start + interval_in_seconds

            sub = Subscription(
                id=sub_id,
                account_id=command.account_id,
                current_period_start=current_period_start,
                current_period_end=current_period_end
            )
            sub_item = SubscriptionItem(
                id=uuid.uuid4().hex,
                sub_id=sub_id,
                price_id=price.id,
            )
            await self._uow.subscription_repository.add(sub)
            await self._uow.subscription_item_repository.add(sub_item)
            await self._uow.commit()
            item_response = ItemResponse(
                item_id=sub_item.id,
                sub_id=sub.id,
                price_id=price.id,
                quantity=sub_item.quantity,
            )
            return CreateSubscriptionResponse(
                sub_id=sub.id,
                account_id=sub.account_id,
                current_period_start=sub.current_period_start,
                current_period_end=sub.current_period_end,
                cancelled=sub.cancelled,
                status=sub.status,
                items=[item_response]
            )