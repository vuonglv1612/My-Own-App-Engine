import uuid
from celery import Celery
from sqlalchemy import select
from core.models import AccountBalance, Transaction, Subscription, InvoiceLine, Invoice, SubscriptionItem, Price, Product
from infrastructure.postgres.connection import create_sync_session_factory
from infrastructure.postgres.mapping import start_mapping
from config import Settings as settings


app = Celery('tasks', broker='redis://14.225.36.41:6379/0')
session_factory = create_sync_session_factory(settings.postgresql_uri)
start_mapping()


interval_mapping = {
    "day": 86400,
    "week": 604800,
    "month": 2592000,
    "year": 31536000,
}

@app.task(name="create_invoice")
def create_invoice(subscription_id):
    print(f"Creating invoice for sub: {subscription_id}")
    with session_factory() as session:
        query = select(Subscription, SubscriptionItem).join(SubscriptionItem, Subscription.id==SubscriptionItem.sub_id).where(Subscription.id==subscription_id)
        result = session.execute(query)
        sub, sub_item = result.fetchone()
        invoice_id = uuid.uuid4().hex
        lines = []
        sub_items = [sub_item]
        invoice_amount = 0
        for sub_item in sub_items:
            query = select(Price, Product.name).join(Price, Product.id==Price.product_id).where(Price.id==sub_item.price_id)
            result = session.execute(query)
            price, product_name = result.fetchone()
            description = f"{product_name} from {sub.current_period_start} to {sub.current_period_end}"
            line_amount = price.line_billing(sub_item.quantity)
            lines.append(InvoiceLine(
                id=uuid.uuid4().hex,
                invoice_id=invoice_id,
                sub_item_id=sub_item.id,
                price_id=sub_item.price_id,
                quantity=sub_item.quantity,
                amount=line_amount,
                description=description
            ))
            invoice_amount += line_amount
        invoice = Invoice(
            id=invoice_id,
            account_id=sub.account_id,
            sub_id=sub.id,
            period_end=sub.current_period_end,
            period_start=sub.current_period_start,
            amount=invoice_amount
        )
        session.add(invoice)
        for line in lines:
            session.add(line)
        session.commit()


@app.task(name="charge_invoice")
def charge_invoice(invoice_id):
    with session_factory() as session:
        query = select(Invoice).where(Invoice.id == invoice_id)
        result = session.execute(query)
        invoice = result.scalar()
        if invoice.status == "paid":
            return
        query = select(Subscription, SubscriptionItem).join(SubscriptionItem, Subscription.id==SubscriptionItem.sub_id).where(Subscription.id==invoice.sub_id)
        result = session.execute(query)
        sub, sub_item = result.fetchone()
        transaction = Transaction(
            account_id=sub.account_id,
            amount=invoice.amount,
            transaction_type="charge_invoice"
        )
        query = select(AccountBalance).where(AccountBalance.account_id == sub.account_id)
        result = session.execute(query)
        account_balance = result.scalar()
        if invoice.amount > account_balance.amount:
            raise Exception("Account balance not enough")
        account_balance.amount = account_balance.amount - invoice.amount
        invoice.status = "paid"
        sub.status = "active"
        query = select(Price).where(Price.id == sub_item.price_id)
        result = session.execute(query)
        price = result.scalar()
        recurring = price.recurring
        sub.current_period_start += interval_mapping[recurring["interval"]]
        sub.current_period_end += interval_mapping[recurring["interval"]]
        sub.current_period_amount = 0

        session.add(sub)
        session.add(invoice)
        session.add(account_balance)
        session.add(transaction)
        session.commit()
