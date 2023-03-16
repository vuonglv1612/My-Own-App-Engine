from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

from src.dependencies import start_mappers
from .routes.app import router as app_router
from .routes.project import router as project_router
from .routes.units import router as units_router
from .routes.user import router as user_router

start_mappers()
app = FastAPI(title="Dashboard API", version="0.1.0", description="Dashboard API")
origins = [
    "http://localhost",
    "http://localhost:9000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", include_in_schema=False)
def read_root():
    return RedirectResponse(url="/docs")


app.include_router(app_router, prefix="/apps", tags=["apps"])
app.include_router(user_router, prefix="/users", tags=["users"])
app.include_router(project_router, prefix="/projects", tags=["projects"])
app.include_router(units_router, prefix="/units", tags=["units"])
