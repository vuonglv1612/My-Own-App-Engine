from datetime import datetime
from typing import Optional

from attrs import define, field

from core.interfaces.unit_of_work import UnitOfWork
from core.models import Product


@define(kw_only=True, slots=False)
class CreateProductCommand:
    name: Optional[str] = field(default=None)
    description: Optional[str] = field(default=None)
    unit_label: Optional[str] = field(default=None)


@define(kw_only=True, slots=False)
class CreateProductResponse:
    id: str = field()
    created_at: datetime = field()
    name: Optional[str] = field(default=None)
    description: Optional[str] = field(default=None)
    unit_label: Optional[str] = field(default=None)


class CreateProductUseCase:
    def __init__(self, unit_of_work: UnitOfWork):
        self._uow = unit_of_work

    async def handle(self, command: CreateProductCommand) -> CreateProductResponse:
        async with self._uow:
            product_id = await self._uow.product_repository.next_id()
            product = Product(
                id=product_id,
                name=command.name,
                description=command.description,
                unit_label=command.unit_label,
            )
            await self._uow.product_repository.add(product)
            await self._uow.commit()
            return CreateProductResponse(
                id=product_id,
                created_at=product.created_at,
                name=command.name,
                description=command.description,
                unit_label=command.unit_label,
            )
