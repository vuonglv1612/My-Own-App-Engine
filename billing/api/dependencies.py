from dependencies import unit_of_work_factory
from celery import Celery

app = Celery('tasks', broker='redis://14.225.36.41:6379/0')

@app.task(name="create_invoice")
def create_invoice(subscription_id):
    ...

async def unit_of_work():
    return unit_of_work_factory()
