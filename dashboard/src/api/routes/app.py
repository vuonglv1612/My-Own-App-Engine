from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, fields

from src.api.auth import check_required_permissions
from src.api.auth import current_project
from src.api.dependencies import unit_of_work
from src.handlers import app as app_handlers

router = APIRouter()


class CreateAppPayload(BaseModel):
    name: str = fields.Field(..., description="App name, must be unique")


class CreateAppResponse(BaseModel):
    id: str = fields.Field(..., description="App id")
    name: str = fields.Field(..., description="App name")
    created_at: datetime = fields.Field(..., description="App creation date")
    deleted_at: Optional[datetime] = fields.Field(..., description="App deletion date")


@router.get("/{app_name}", dependencies=[Depends(check_required_permissions(["apps:read"]))])
async def get_app(app_name: str):
    return {"app_name": app_name}


@router.post("", dependencies=[Depends(check_required_permissions(["apps:write"]))], response_model=CreateAppResponse)
async def create_app(
    body: CreateAppPayload,
    uow=Depends(unit_of_work),
    project=Depends(current_project),
):
    try:
        app = await app_handlers.new_app(uow, project_id=project.id, app_name=body.name)
    except ValueError as e:
        raise HTTPException(status_code=400, detail={"error": str(e)})
    return app
