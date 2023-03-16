from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, Depends
from pydantic.main import BaseModel

from src.api.auth import current_user
from src.api.dependencies import unit_of_work, get_billing_client
from src.core.entities import User
from src.core.services.create_user import CreateUserCommand, CreateUserUserCase
from src.core.services.list_projects_by_user import ListProjectByUserCommand, ListProjectByUserUseCase

router = APIRouter()


class CreateUserBody(BaseModel):
    sub: str
    email: str
    name: Optional[str] = None


@router.post("")
async def create_user(body: CreateUserBody, uow=Depends(unit_of_work), billing_client=Depends(get_billing_client)):
    command = CreateUserCommand(name=body.name, email=body.email, sub=body.sub)
    user_case = CreateUserUserCase(uow, billing_client)
    user = await user_case.execute(command)
    return user


class ProjectResponse(BaseModel):
    id: str
    name: str
    created_at: datetime
    role: str


class MetaResponse(BaseModel):
    total: int
    page: int
    per_page: int


class ListProjectByUserResponse(BaseModel):
    items: List[ProjectResponse]
    meta: MetaResponse


@router.get("/me/projects")
async def list_projects_by_user(page: int = 1, per_page: int = 10, uow=Depends(unit_of_work),
                                user: User = Depends(current_user)):
    user_id = user.id
    command = ListProjectByUserCommand(user_id=user_id, page=page, per_page=per_page)
    use_case = ListProjectByUserUseCase(uow)
    projects = await use_case.execute(command)
    return projects
