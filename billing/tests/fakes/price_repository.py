from core.interfaces.repositories import PriceRepository


class FakePriceRepository(PriceRepository):
    def __init__(self):
        self.prices = {}

    async def next_id(self) -> str:
        return "fake_price_id"

    async def add(self, price):
        self.prices[price.id] = price

    async def get(self, price_id):
        return self.prices.get(price_id)
