from typing import Optional

import sqlalchemy.exc
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, fields

from src.api.auth import current_user
from src.api.dependencies import unit_of_work, get_provisioner, get_deploy_client
from src.core.services.create_app import CreateAppCommand, CreateAppUseCase
from src.core.services.delete_app import DeleteAppUseCase, DeleteAppCommand
from src.core.services.deploy_an_app import DeployAppCommand, DeployAppUseCase
from src.core.services.resize_app import ScaleAppUseCase, ScaleAppCommand
from src.services.provisioner import Provisioner
from src.services.unit_of_work import UnitOfWork

router = APIRouter()


class CreateAppPayload(BaseModel):
    project_id: str = fields.Field(..., description="Project id")
    name: str = fields.Field(..., description="App name, must be unique")
    description: Optional[str] = fields.Field("", description="App description")
    unit: str = fields.Field(..., description="App unit")
    replicas: int = fields.Field(..., description="App replicas", example=1)
    platform: str = fields.Field("python", description="App platform")


@router.post("")
async def create_app(
        body: CreateAppPayload,
        uow=Depends(unit_of_work),
        provisioner=Depends(get_provisioner),
        user=Depends(current_user)
):
    handler = CreateAppUseCase(uow, provisioner)
    try:
        command = CreateAppCommand(
            user=user,
            name=body.name,
            project_id=body.project_id,
            unit=body.unit,
            replicas=body.replicas,
            platform=body.platform,
            description=body.description
        )
        app = await handler.handle(command)
    except ValueError as e:
        raise HTTPException(status_code=400, detail={"error": str(e)})
    except sqlalchemy.exc.IntegrityError:
        raise HTTPException(status_code=400, detail={"error": "App name already exists"})
    return app


class DeployAppPayload(BaseModel):
    project_id: str = fields.Field(..., description="Project id")
    version: str = fields.Field(..., description="App version")
    source_type: str = fields.Field(..., description="App source type", example="git")
    source_url: str = fields.Field(..., description="App source url")
    git_branch: Optional[str] = fields.Field("master", description="App git branch")


@router.post("/{app_name}/deploy")
async def deploy_app(
        app_name: str,
        body: DeployAppPayload,
        uow=Depends(unit_of_work),
        deploy_client=Depends(get_deploy_client),
        user=Depends(current_user)
):
    handler = DeployAppUseCase(uow, deploy_client)
    try:
        command = DeployAppCommand(
            user=user,
            app_id=app_name,
            project_id=body.project_id,
            version=body.version,
            source_type=body.source_type,
            source_url=body.source_url,
            git_branch=body.git_branch
        )
        app = await handler.handle(command)
    except ValueError as e:
        raise HTTPException(status_code=400, detail={"error": str(e)})
    return app


@router.get("/{app_name}/envs")
async def get_app_envs(
        app_name: str,
        page: int = 1,
        page_size: int = 10,
        uow: UnitOfWork = Depends(unit_of_work),
        user=Depends(current_user),
):
    async with uow:
        app = await uow.apps.get_by_id(app_name)
        if not app:
            raise HTTPException(status_code=404, detail={"error": "App not found"})
        project = await uow.projects.get_by_id(app.project_id)
        if not project:
            raise HTTPException(status_code=404, detail={"error": "App not found"})
        if project.is_member(user.id) is False:
            raise HTTPException(status_code=403, detail={"error": "Permission denied"})
        envs, total = await uow.environments.list_app_environments(app_name, page, page_size)
        return {
            "items": [{
                "id": env.id,
                "name": env.name,
                "app_id": env.app_id,
                "value": env.value,
            } for env in envs],
            "meta": {
                "total": total,
                "page": page,
                "page_size": page_size
            }
        }


# Delete app envs
@router.delete("/{app_name}/envs/{env_id}")
async def delete_app_env(
        app_name: str,
        env_id: str,
        uow: UnitOfWork = Depends(unit_of_work),
        provisioner: Provisioner = Depends(get_provisioner),
        user=Depends(current_user)
):
    async with uow:
        app = await uow.apps.get_by_id(app_name)
        if not app:
            raise HTTPException(status_code=404, detail={"error": "App not found"})
        project = await uow.projects.get_by_id(app.project_id)
        if not project:
            raise HTTPException(status_code=404, detail={"error": "App not found"})
        if project.is_member(user.id) is False:
            raise HTTPException(status_code=403, detail={"error": "Permission denied"})
        env = await uow.environments.get_by_id(env_id)
        if not env:
            raise HTTPException(status_code=404, detail={"error": "Env not found"})
        await provisioner.delete_env(app_name, env.name)
        await uow.environments.delete(env)
        await uow.commit()
    return {"message": "ok"}


class CreateEnvPayload(BaseModel):
    name: str = fields.Field(..., description="Env name, must be unique")
    value: str = fields.Field(..., description="Env value")


# Create app envs
@router.post("/{app_name}/envs")
async def create_app_env(
        app_name: str,
        body: CreateEnvPayload,
        uow: UnitOfWork = Depends(unit_of_work),
        provisioner: Provisioner = Depends(get_provisioner),
        user=Depends(current_user)
):
    async with uow:
        app = await uow.apps.get_by_id(app_name)
        if not app:
            raise HTTPException(status_code=404, detail={"error": "App not found"})
        project = await uow.projects.get_by_id(app.project_id)
        if not project:
            raise HTTPException(status_code=404, detail={"error": "App not found"})
        if project.is_member(user.id) is False:
            raise HTTPException(status_code=403, detail={"error": "Permission denied"})
        env = await uow.environments.get_by_name(body.name)
        if env:
            raise HTTPException(status_code=400, detail={"error": "Biến đã tồn tại"})
        await provisioner.set_env(app_name, body.name, body.value)
        await uow.environments.create(body.name, body.value, app)
        await uow.commit()
    return {"message": "ok"}


# update app envs
class UpdateEnvPayload(BaseModel):
    value: str = fields.Field(..., description="Env value")


@router.put("/{app_name}/envs/{env_id}")
async def update_app_env(
        app_name: str,
        env_id: str,
        body: UpdateEnvPayload,
        uow: UnitOfWork = Depends(unit_of_work),
        provisioner: Provisioner = Depends(get_provisioner),
        user=Depends(current_user)
):
    async with uow:
        app = await uow.apps.get_by_id(app_name)
        if not app:
            raise HTTPException(status_code=404, detail={"error": "App not found"})
        env = await uow.environments.get_by_id(env_id)
        if not env:
            raise HTTPException(status_code=404, detail={"error": "Env not found"})
        project = await uow.projects.get_by_id(app.project_id)
        if not project:
            raise HTTPException(status_code=404, detail={"error": "App not found"})
        if project.is_member(user.id) is False:
            raise HTTPException(status_code=403, detail={"error": "Permission denied"})
        env.value = body.value
        await provisioner.set_env(app_name, env.name, body.value)
        await uow.commit()
    return {"message": "ok"}


# Delete app
@router.delete("/{app_name}")
async def delete_app(
        app_name: str,
        uow=Depends(unit_of_work),
        provisioner=Depends(get_provisioner),
        user=Depends(current_user)
):
    handler = DeleteAppUseCase(uow, provisioner)
    try:
        command = DeleteAppCommand(
            user=user,
            app_id=app_name,
        )
        app = await handler.handle(command)
    except ValueError as e:
        raise HTTPException(status_code=400, detail={"error": str(e)})
    return app


# Scale app
class ScaleAppPayload(BaseModel):
    replicas: int = fields.Field(..., description="Replicas count")


@router.post("/{app_name}/scale")
async def scale_app(
        app_name: str,
        body: ScaleAppPayload,
        uow=Depends(unit_of_work),
        deploy_client=Depends(get_deploy_client),
        user=Depends(current_user)
):
    handler = ScaleAppUseCase(uow, deploy_client)
    try:
        command = ScaleAppCommand(
            user=user,
            app_id=app_name,
            replicas=body.replicas
        )
        app = await handler.execute(command)
    except ValueError as e:
        raise HTTPException(status_code=400, detail={"error": str(e)})
    return app


@router.post("/{app_name}/restart")
async def restart_app(
        app_name: str,
        uow: UnitOfWork = Depends(unit_of_work),
        deploy_client=Depends(get_deploy_client),
        user=Depends(current_user)
):
    try:
        async with uow:
            app = await uow.apps.get_by_id(app_name)
            if not app:
                raise HTTPException(status_code=404, detail={"error": "App not found"})
            project = await uow.projects.get_by_id(app.project_id)
            if not project:
                raise HTTPException(status_code=404, detail={"error": "App not found"})
            if project.is_member(user.id) is False:
                raise HTTPException(status_code=403, detail={"error": "Permission denied"})
            app.run()
            await uow.apps.add(app)
            await uow.commit()
            await deploy_client.restart_app(app_name)
    except ValueError as e:
        raise HTTPException(status_code=400, detail={"error": str(e)})
    return app


@router.post("/{app_name}/stop")
async def stop_app(
        app_name: str,
        uow: UnitOfWork = Depends(unit_of_work),
        deploy_client=Depends(get_deploy_client),
        user=Depends(current_user)
):
    try:
        async with uow:
            app = await uow.apps.get_by_id(app_name)
            if not app:
                raise HTTPException(status_code=404, detail={"error": "App not found"})
            project = await uow.projects.get_by_id(app.project_id)
            if not project:
                raise HTTPException(status_code=404, detail={"error": "App not found"})
            if project.is_member(user.id) is False:
                raise HTTPException(status_code=403, detail={"error": "Permission denied"})
            app.stop()
            await uow.apps.add(app)
            await uow.commit()
            await deploy_client.stop_app(app_name)
    except ValueError as e:
        raise HTTPException(status_code=400, detail={"error": str(e)})
    return app
