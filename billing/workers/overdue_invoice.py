from sqlalchemy import select

from core.models import Invoice, Subscription
from utils.datetime import aware_now


class OverdueInvoiceWorker:

    def __init__(self, async_session):
        self._async_session = async_session

    async def handle_invoice(self):
        print("Fetching invoice")
        async with self._async_session() as session:
            query = select(Invoice).where(Invoice.due >= aware_now(), Invoice.status != "overdue")
            result = await session.execute(query)
            invoices = result.all()
            for invoice, in invoices:
                print(f"handle invoice {invoice.id}")
                query = select(Subscription).where(Subscription.id == invoice.sub_id)
                result = await session.execute(query)
                sub = result.scalar()
                invoice.status = "overdue"
                sub.status = "closed"
                #TODO: send webhook
                session.add(invoice)
                session.add(sub)
                await session.commit()

    async def _send_webhook(self, event_type, sub):
        ...