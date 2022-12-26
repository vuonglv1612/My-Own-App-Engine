from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from .routes.app import router as app_router

app = FastAPI()


@app.get("/", include_in_schema=False)
def read_root():
    return RedirectResponse(url="/docs")


app.include_router(app_router, prefix="/test_cases", tags=["test_cases"])
