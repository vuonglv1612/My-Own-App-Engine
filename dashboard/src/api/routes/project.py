from attrs import asdict
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from src.api.auth import current_user
from src.api.dependencies import unit_of_work, get_billing_client
from src.core.entities import User, ProjectMember
from src.core.services.create_project import CreateProjectCommand, CreateProjectUseCase
from src.services.unit_of_work import UnitOfWork

router = APIRouter()


class CreateProjectBody(BaseModel):
    name: str


# create new project with name
@router.post("")
async def create_project(body: CreateProjectBody, uow=Depends(unit_of_work), user: User = Depends(current_user),
                         billing_client=Depends(get_billing_client)):
    command = CreateProjectCommand(name=body.name, user_id=user.id)
    use_case = CreateProjectUseCase(uow, billing_client)
    try:
        project = await use_case.execute(command)
    except ValueError as e:
        raise HTTPException(status_code=400, detail={"error": str(e)})
    return project


@router.get("/{project_id}/apps/{app_name}")
async def get_app(app_name: str, project_id: str, uow: UnitOfWork = Depends(unit_of_work),
                  user: User = Depends(current_user)):
    async with uow:
        project = await uow.projects.get_by_id(project_id)
        if not project:
            raise HTTPException(status_code=404, detail={"error": "Project not found"})
        is_member = project.is_member(user.id)
        if not is_member:
            raise HTTPException(status_code=403, detail={"error": "You are not member of this project"})
        app = await uow.apps.get_by_name(app_name, project_id=project_id)
        if not app:
            raise HTTPException(status_code=404, detail={"error": "App not found"})
        return {
            "id": app.id,
            "name": app.name,
            "status": app.status,
            "description": app.description,
            "platform": app.platform,
            "created_at": app.created_at,
            "updated_at": app.created_at,
        }


@router.get("/{project_id}/apps")
async def get_apps(project_id: str, page: int = 1, page_size: int = 10, uow: UnitOfWork = Depends(unit_of_work),
                   user: User = Depends(current_user)):
    async with uow:
        project = await uow.projects.get_by_id(project_id)
        if not project:
            raise HTTPException(status_code=404, detail={"error": "Project not found"})
        is_member = project.is_member(user.id)
        if not is_member:
            raise HTTPException(status_code=403, detail={"error": "You are not member of this project"})
        apps, total = await uow.apps.list_app_in_project(project_id=project_id, page=page, page_size=page_size)
        response = {
            "items": [{
                "id": app.id,
                "name": app.name,
                "status": app.status,
                "platform": app.platform,
                "description": app.description,
                "created_at": app.created_at.isoformat(),
                "updated_at": app.created_at.isoformat(),
            } for app in apps],
            "meta": {
                "total": total,
                "page": page,
                "page_size": page_size
            }
        }
        return response


@router.get("/{project_id}/apps/{app_name}/activities")
async def list_app_activities(app_name: str, page: int = 1, page_size: int = 20,
                              uow: UnitOfWork = Depends(unit_of_work)):
    async with uow:
        activities, total = await uow.activities.list_app_activity(app_id=app_name, page=page,
                                                                   page_size=page_size)
        response = {
            "items": [{
                "id": activity.id,
                "app_id": activity.app_id,
                "event": activity.event,
                "created_at": activity.created_at.isoformat(),
                "event_type": activity.event_type,
                "actor": activity.actor,
            } for activity in activities],
            "meta": {
                "total": total,
                "page": page,
                "page_size": page_size
            }
        }
        return response


# Leave project
@router.delete("/{project_id}/members/me")
async def leave_project(project_id: str, uow: UnitOfWork = Depends(unit_of_work),
                        user: User = Depends(current_user)):
    async with uow:
        project = await uow.projects.get_by_id(project_id)
        if not project:
            raise HTTPException(status_code=404, detail={"error": "Project not found"})
        is_member = project.is_member(user.id)
        if not is_member:
            raise HTTPException(status_code=403, detail={"error": "You are not member of this project"})
        is_owner = project.is_owner(user.id)
        if is_owner:
            raise HTTPException(status_code=403, detail={"error": "You are owner of this project"})
        await uow.projects.remove_member(project_id, user.id)
        await uow.commit()
        return {"message": "OK"}


# remove member from project
@router.delete("/{project_id}/members/{user_id}")
async def remove_member(project_id: str, user_id: str, uow: UnitOfWork = Depends(unit_of_work),
                        user: User = Depends(current_user)):
    async with uow:
        project = await uow.projects.get_by_id(project_id)
        if not project:
            raise HTTPException(status_code=404, detail={"error": "Project not found"})
        is_member = project.is_member(user.id)
        if not is_member:
            raise HTTPException(status_code=403, detail={"error": "Bạn không phải là thành viên của dự án này"})
        is_admin = project.is_admin(user.id)
        if not is_admin:
            raise HTTPException(status_code=403, detail={"error": "Bạn không phải là quản trị viên của dự án này"})
        if project.is_owner(user_id):
            raise HTTPException(status_code=403, detail={"error": "Không thể xóa chủ sở hữu dự án"})
        await uow.projects.remove_member(project_id, user_id)
        await uow.commit()
        return {"message": "OK"}


@router.get("/{project_id}/members")
async def list_members(project_id: str, page: int = 1, page_size: int = 20, uow: UnitOfWork = Depends(unit_of_work),
                       user: User = Depends(current_user)):
    async with uow:
        project = await uow.projects.get_by_id(project_id)
        if not project:
            raise HTTPException(status_code=404, detail={"error": "Project not found"})
        is_member = project.is_member(user.id)
        if not is_member:
            raise HTTPException(status_code=403, detail={"error": "You are not member of this project"})
        members, total = await uow.projects.list_members(project_id=project_id, page=page, page_size=page_size)
        response = {
            "items": [{
                "id": member.id,
                "role": member.role,
                "created_at": member.created_at.isoformat(),
                "user_id": member.user_id,
                "user": {
                    "name": member.user.name,
                    "email": member.user.email
                },
                "project_id": member.project_id,
            } for member in members],
            "meta": {
                "total": total,
                "page": page,
                "page_size": page_size
            }
        }
        return response


# add member to project

class AddMemberBody(BaseModel):
    email: str


@router.post("/{project_id}/members")
async def add_member(body: AddMemberBody, project_id: str, uow: UnitOfWork = Depends(unit_of_work),
                     user: User = Depends(current_user)):
    async with uow:
        project = await uow.projects.get_by_id(project_id)
        if not project:
            raise HTTPException(status_code=404, detail={"error": "Project not found"})
        is_member = project.is_member(user.id)
        if not is_member:
            raise HTTPException(status_code=403, detail={"error": "You are not member of this project"})
        body_user = await uow.users.get_by_email(body.email)
        if not body_user:
            raise HTTPException(status_code=404, detail={"error": "Không tìm thấy người dùng"})
        if project.is_member(body_user.id):
            raise HTTPException(status_code=400, detail={"error": "Người dùng đã là thành viên"})
        member = ProjectMember(project_id=project_id, user_id=body_user.id, role="member")
        await uow.project_members.add(member)
        await uow.commit()
        return asdict(member)


class ChangeRoleBody(BaseModel):
    role: str


# Change role of member
@router.put("/{project_id}/members/{user_id}")
async def change_role(project_id: str, user_id: str, body: ChangeRoleBody, uow: UnitOfWork = Depends(unit_of_work),
                      user: User = Depends(current_user)):
    async with uow:
        project = await uow.projects.get_by_id(project_id)
        if not project:
            raise HTTPException(status_code=404, detail={"error": "Project not found"})
        is_member = project.is_member(user.id)
        if not is_member:
            raise HTTPException(status_code=403, detail={"error": "Bạn không phải là thành viên của dự án"})
        is_admin = project.is_admin(user.id)
        if not is_admin:
            raise HTTPException(status_code=403, detail={"error": "Bạn không phải là quản trị viên của dự án"})
        if body.role not in ["member", "admin"]:
            raise HTTPException(status_code=400, detail={"error": "Role không hợp lệ"})
        project_member = await uow.project_members.get_by_project_and_user(project_id, user_id)
        if not project_member:
            raise HTTPException(status_code=404, detail={"error": "Thành viên không tồn tại"})
        if not project.is_member(project_member.user_id):
            raise HTTPException(status_code=400, detail={"error": "Thành viên không tồn tại"})
        if project.is_owner(project_member.user_id):
            raise HTTPException(status_code=400, detail={"error": "Không thể thay đổi quyền của chủ sở hữu"})
        project_member.role = body.role
        await uow.project_members.add(project_member)
        await uow.commit()
        return asdict(project_member)


# Delete project
@router.delete("/{project_id}")
async def delete_project(project_id: str, uow: UnitOfWork = Depends(unit_of_work),
                         user: User = Depends(current_user)):
    async with uow:
        project = await uow.projects.get_by_id(project_id)
        if not project:
            raise HTTPException(status_code=404, detail={"error": "Project not found"})
        is_owner = project.is_owner(user.id)
        if not is_owner:
            raise HTTPException(status_code=403, detail={"error": "Bạn không phải là chủ sở hữu của dự án"})
        if project.name == user.name:
            raise HTTPException(status_code=400, detail={"error": "Bạn không thể xóa dự án mặc định"})
        await uow.projects.delete(project)
        await uow.commit()
        return {"message": "OK"}


# get app active scale
@router.get("/{project_id}/apps/{app_name}/active-scale")
async def get_app_scale(
        project_id: str,
        app_name: str,
        uow=Depends(unit_of_work),
        user=Depends(current_user)
):
    async with uow:
        project = await uow.projects.get_by_id(project_id)
        if not project:
            raise HTTPException(status_code=404, detail={"error": "Project not found"})
        is_member = project.is_member(user.id)
        if not is_member:
            raise HTTPException(status_code=403, detail={"error": "You are not member of this project"})
        app = await uow.apps.get_by_name(app_name=app_name, project_id=project_id)
        if not app:
            raise HTTPException(status_code=404, detail={"error": "App not found"})
        scale = await uow.scales.get_active_by_app_id(app.id)
        if not scale:
            raise HTTPException(status_code=404, detail={"error": "Scale not found"})
        return asdict(scale)


# list app scales
@router.get("/{project_id}/apps/{app_name}/scales")
async def list_app_scales(
        project_id: str,
        app_name: str,
        page: int = 1,
        page_size: int = 10,
        uow=Depends(unit_of_work),
        user=Depends(current_user)
):
    async with uow:
        project = await uow.projects.get_by_id(project_id)
        if not project:
            raise HTTPException(status_code=404, detail={"error": "Project not found"})
        is_member = project.is_member(user.id)
        if not is_member:
            raise HTTPException(status_code=403, detail={"error": "You are not member of this project"})
        app = await uow.apps.get_by_name(app_name=app_name, project_id=project_id)
        if not app:
            raise HTTPException(status_code=404, detail={"error": "App not found"})
        scales, total = await uow.scales.list_by_app_id(app_id=app.id, page=page, page_size=page_size)
        response = {
            "data": [asdict(scale) for scale in scales],
            "meta": {
                "total": total,
                "page": page,
                "page_size": page_size
            }
        }
        return response
