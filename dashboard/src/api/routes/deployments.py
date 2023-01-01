from typing import Dict

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, fields

from src.api.auth import check_required_permissions, current_project
from src.api.dependencies import unit_of_work, get_provisioner

router = APIRouter()


class CreateDeploymentPayload(BaseModel):
    app_name: str = fields.Field(..., description="App name")
    image: str = fields.Field(..., description="Image name")
    envs: Dict[str, str] = fields.Field(..., description="Environment variables")


@router.post("", dependencies=[Depends(check_required_permissions(["deployments:write"]))])
async def create_deployment(
    body: CreateDeploymentPayload,
    uow=Depends(unit_of_work),
    provisioner=Depends(get_provisioner),
    project=Depends(current_project),
):
    try:
        app = await deployment_handlers.new(
            uow,
            provisioner,
            project_id=project.id,
            app_name=body.app_name,
            image=body.image,
            envs=body.envs,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail={"error": str(e)})
    return app
