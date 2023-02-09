from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from .routes import account
from .routes import price
from .routes import product
from .routes import subscription
from .routes import usage
from .routes import invoices
from .routes import topup
from .routes import transaction

app = FastAPI()


@app.get("/", include_in_schema=False)
def read_root():
    return RedirectResponse(url="/docs")


app.include_router(account.router, prefix="/accounts", tags=["account"])
app.include_router(product.router, prefix="/products", tags=["product"])
app.include_router(price.router, prefix="/prices", tags=["price"])
app.include_router(subscription.router, prefix="/subscriptions", tags=["subscription"])
app.include_router(usage.router, prefix="/usage", tags=["usage"])
app.include_router(invoices.router, prefix="/invoices", tags=["invoices"])
app.include_router(topup.router, prefix="/topups", tags=["topups"])
app.include_router(transaction.router, prefix="/transactions", tags=["transactions"])