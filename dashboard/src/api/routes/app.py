from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, fields

from src.api.auth import check_required_permissions
from src.api.auth import current_project
from src.api.dependencies import unit_of_work, get_provisioner
from src.handlers import app as app_handlers

router = APIRouter()


class CreateAppPayload(BaseModel):
    name: str = fields.Field(..., description="App name, must be unique")
    plan: str = fields.Field(description="The plan name for the test_cases")


class CreateAppResponse(BaseModel):
    id: str = fields.Field(..., description="App id")
    name: str = fields.Field(..., description="App name")
    project_id: str = fields.Field(..., description="Project id")
    plan: str = fields.Field(..., description="The plan name for the test_cases")
    status: str = fields.Field(..., description="App status")
    created_at: str = fields.Field(..., description="App creation date")
    deleted_at: str = fields.Field(..., description="App deletion date")


@router.get("/{app_name}", dependencies=[Depends(check_required_permissions(["test_cases:read"]))])
async def get_app(app_name: str):
    return {"app_name": app_name}


@router.post("/", dependencies=[Depends(check_required_permissions(["test_cases:write"]))])
async def create_app(
    body: CreateAppPayload,
    uow=Depends(unit_of_work),
    provisioner=Depends(get_provisioner),
    project=Depends(current_project),
):
    try:
        app = await app_handlers.new_app(uow, provisioner, project_id=project.id, app_name=body.name, plan=body.plan)
    except ValueError as e:
        raise HTTPException(status_code=400, detail={"error": str(e)})
    return app
