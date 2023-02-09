from attrs import define, field

from core.interfaces.unit_of_work import UnitOfWork
from core.errors import subscriptions

@define(kw_only=True, slots=False)
class ReportUsageCommand:
    subscription_item_id: str = field()
    timestamp: int = field()
    quantity: int = field()


@define(kw_only=True, slots=False)
class ReportUsageResponse:
    ...


class ReportUsageUseCase:
    def __init__(self, unit_of_work: UnitOfWork, create_invoice_task) -> None:
        self._uow = unit_of_work
        self._create_invoice_task = create_invoice_task

    async def handle(self, command: ReportUsageCommand) -> ReportUsageResponse:
        async with self._uow:
            sub_item = await self._uow.subscription_item_repository.get(command.subscription_item_id)
            if not sub_item:
                raise subscriptions.SubscriptionItemNotFound
            try:
                price = await self._uow.price_repository.get(sub_item.price_id)
                sub_item.quantity = command.quantity + sub_item.quantity
                sub = await self._uow.subscription_repository.get(sub_item.sub_id)
                if command.timestamp not in range(sub.current_period_start, sub.current_period_end+1):
                    return False
                amount = price.billing(command.quantity)
                sub.current_period_amount += amount
                account_balance = await self._uow.account_balance_repository.get_by_account_id(sub.account_id)
                if account_balance.amount <= sub.current_period_amount:
                    self._create_invoice_task.delay(sub.id)
                await self._uow.subscription_item_repository.add(sub_item)
                await self._uow.subscription_repository.add(sub)
                await self._uow.commit()
                return True
            except Exception as e:
                print(f"Error while reporting usage {e}")
                return False
