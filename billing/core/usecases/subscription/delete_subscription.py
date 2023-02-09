from datetime import datetime, timedelta
from typing import List, Optional

from attrs import define, field
from utils.datetime import aware_now

from core.interfaces.unit_of_work import UnitOfWork
from core.models import Subscription
from core.errors import subscriptions

@define(kw_only=True, slots=False)
class DeleteSubscriptionCommand:
    sub_id: str = field()


@define(kw_only=True, slots=False)
class DeleteSubscriptionResponse:
    sub_id: str = field()
    status: str = field()


class DeleteSubscriptionUseCase:
    def __init__(self, unit_of_work: UnitOfWork):
        self._uow = unit_of_work

    async def handle(self, command: DeleteSubscriptionCommand) -> DeleteSubscriptionResponse:
        async with self._uow:
            sub = await self._uow.subscription_repository.get(command.sub_id)
            if not sub:
                raise subscriptions.SubscriptionNotFound
            dt = datetime.now()
            sub.cancel_at = datetime.timestamp(dt)
            sub.status = "cancelled"
            sub.cancelled = True
            await self._uow.subscription_repository.add(sub)
            await self._uow.commit()
            #call webhook to delete
            return DeleteSubscriptionResponse(
                sub_id=sub.id,
                status=sub.status,
            )