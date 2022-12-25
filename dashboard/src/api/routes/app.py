from attrs import asdict
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, fields

from src.api.auth import check_required_permissions
from src.api.auth import current_project
from src.api.dependencies import unit_of_work
from src.handlers import app as app_handlers

router = APIRouter()


class CreateAppPayload(BaseModel):
    name: str = fields.Field(..., description="App name, must be unique")
    plan: str = fields.Field(description="The plan name for the app")


@router.get("/{app_name}", dependencies=[Depends(check_required_permissions(["app:read"]))])
async def get_app(app_name: str):
    return {"app_name": app_name}


@router.post("/", dependencies=[Depends(check_required_permissions(["app:write"]))])
async def create_app(body: CreateAppPayload, uow=Depends(unit_of_work), project=Depends(current_project)):
    try:
        app = await app_handlers.create_app(uow, project_id=project.id, app_name=body.name, plan=body.plan)
    except ValueError as e:
        raise HTTPException(status_code=400, detail={"error": str(e)})
    return asdict(app)
