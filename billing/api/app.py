from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from .routes import account

app = FastAPI()


@app.get("/", include_in_schema=False)
def read_root():
    return RedirectResponse(url="/docs")


app.include_router(account.router, prefix="/accounts", tags=["account"])
