from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from .routes.app import router as app_router
from .routes.deployments import router as deployments_router

app = FastAPI(title="Dashboard API", version="0.1.0", description="Dashboard API")


@app.get("/", include_in_schema=False)
def read_root():
    return RedirectResponse(url="/docs")


app.include_router(app_router, prefix="/apps", tags=["apps"])
app.include_router(deployments_router, prefix="/deployments", tags=["deployments"])
