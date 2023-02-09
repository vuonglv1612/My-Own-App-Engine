from config import Settings as settings
from infrastructure.postgres.connection import create_session_factory
from infrastructure.postgres.mapping import start_mapping
from workers.overdue_invoice import OverdueInvoiceWorker
import asyncio


async def job(session_factory):
    worker = OverdueInvoiceWorker(session_factory)
    await worker.handle_invoice()


async def schedule_job():
    session_factory = create_session_factory(settings.async_postgresql_uri)
    start_mapping()
    while True:
        # schedule the job to run in 3 seconds
        await asyncio.sleep(settings.overdue_invoice_schedule_interval)
        await asyncio.ensure_future(job(session_factory))


if __name__ == '__main__':
    evtlp = asyncio.new_event_loop()
    asyncio.set_event_loop(evtlp)
    asyncio.run(schedule_job())
