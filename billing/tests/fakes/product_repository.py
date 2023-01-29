import uuid

from core.interfaces.repositories import ProductRepository


class FakeProductRepository(ProductRepository):
    def __init__(self):
        self._products = {}

    async def add(self, product):
        self._products[product.id] = product

    async def get(self, product_id):
        return self._products.get(product_id)

    async def next_id(self) -> str:
        return str(uuid.uuid4().hex)
