from typing import Optional

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field, EmailStr

from api.dependencies import unit_of_work
from core.usecases import account as account_usecases
from infrastructure.services.unit_of_work import UnitOfWork

router = APIRouter()


class CreateAccountBody(BaseModel):
    name: Optional[str] = Field(None, max_length=255, description="The name of the account")
    address: Optional[str] = Field(None, max_length=255, description="The address of the account")
    description: Optional[str] = Field(None, max_length=255, description="The description of the account")
    email: Optional[EmailStr] = Field(None, description="The email of the account")
    phone: Optional[str] = Field(None, max_length=255, description="The phone number of the account")


@router.post("")
async def create_account(body: CreateAccountBody, uow: UnitOfWork = Depends(unit_of_work)):
    """
    Create a new account
    """
    command = account_usecases.CreateAccountCommand(
        name=body.name,
        address=body.address,
        description=body.description
    )
    handler = account_usecases.CreateAccountUseCase(uow)
    response = await handler.handle(command)
    return response
