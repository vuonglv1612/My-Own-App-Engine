from typing import Optional

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from api.dependencies import unit_of_work
from core.interfaces.unit_of_work import UnitOfWork
from core.usecases.product.create_product import CreateProductCommand, CreateProductUseCase

router = APIRouter()


class CreateProductBody(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    unit_label: Optional[str] = None


@router.post("")
async def create_product(body: CreateProductBody, uow: UnitOfWork = Depends(unit_of_work)):
    """
    Create a new product
    """
    command = CreateProductCommand(
        name=body.name,
        description=body.description,
        unit_label=body.unit_label,
    )
    handler = CreateProductUseCase(uow)
    response = await handler.handle(command)
    return response
