from datetime import datetime
from typing import Optional

from attrs import asdict
from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field

from api.dependencies import unit_of_work
from core.interfaces.unit_of_work import UnitOfWork
from core.usecases.product.create_product import CreateProductCommand, CreateProductUseCase

router = APIRouter()


class CreateProductBody(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    unit_label: Optional[str] = None


class CreateProductResponse(BaseModel):
    id: str = Field(..., example="product_id")
    created_at: datetime = Field(..., example="2021-01-01T00:00:00Z")
    name: str = Field(..., example="CPU")
    description: str = Field(..., example="CPU")
    unit_label: str = Field(..., example="Core")


@router.post("", response_model=CreateProductResponse)
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
    return asdict(response)
