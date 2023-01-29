from typing import Type

from core.interfaces.repositories import ProductRepository
from core.models import Product
from .repository import SqlalchemyRepository


class SqlalchemyProductRepository(ProductRepository, SqlalchemyRepository[Product]):
    @property
    def entity(self) -> Type[Product]:
        return Product
