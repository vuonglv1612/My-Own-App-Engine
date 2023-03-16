from fastapi import FastAPI, Depends
from pydantic import BaseModel

from task_manager import TaskManager
from .dependencies import get_task_manager

app = FastAPI()


class DeployGitProject(BaseModel):
    deployment_id: str
    app_name: str
    git_url: str
    git_branch: str
    plan_name: str
    replicas: int = 1


@app.post("/deploy-git")
def deploy_git(body: DeployGitProject, task_manager: TaskManager = Depends(get_task_manager)):
    task_manager.send_task("deploy_git_app", body.dict())
    return {"status": "ok"}


class DeployImageProject(BaseModel):
    deployment_id: str
    app_name: str
    image: str
    plan_name: str
    replicas: int = 1


@app.post("/deploy-image")
def deploy_image(body: DeployImageProject, task_manager: TaskManager = Depends(get_task_manager)):
    task_manager.send_task("deploy_image_app", body.dict())
    return {"status": "ok"}


class ScaleApp(BaseModel):
    app_name: str
    change: int


@app.post("/scale")
def scale(body: ScaleApp, task_manager: TaskManager = Depends(get_task_manager)):
    task_manager.send_task("scale_app", {"app_name": body.app_name, "change": body.change})
    return {"status": "ok"}


class StopApp(BaseModel):
    app_name: str


@app.post("/stop")
def stop(body: StopApp, task_manager: TaskManager = Depends(get_task_manager)):
    task_manager.send_task("stop_app", {"app_name": body.app_name})
    return {"status": "ok"}


class RestartApp(BaseModel):
    app_name: str


@app.post("/restart")
def restart(body: RestartApp, task_manager: TaskManager = Depends(get_task_manager)):
    task_manager.send_task("restart_app", {"app_name": body.app_name})
    return {"status": "ok"}
