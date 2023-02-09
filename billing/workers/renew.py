import time
from sqlalchemy import select

from core.models import Subscription


class RenewSubscriptionWorker:

    def __init__(self, async_session, create_invoice):
        self._async_session = async_session
        self._create_invoice = create_invoice

    async def handle(self):
        print("Fetching subscription")
        async with self._async_session() as session:
            query = select(Subscription).where(Subscription.current_period_end >= time.time(), Subscription.status == "active")
            result = await session.execute(query)
            subs = result.all()
            for sub, in subs:
                print(f"renewing subscription {sub.id}")
                sub.status = "renew"
                session.add(sub)
                self._create_invoice.delay(sub.id)
            await session.commit()
