from typing import Type, Optional

from core.interfaces.repositories import PriceRepository
from core.models.prices import Price, PriceRecurring, PriceTier
from .repository import SqlalchemyRepository


class SqlalchemyPriceRepository(PriceRepository, SqlalchemyRepository[Price]):
    @property
    def entity(self) -> Type[Price]:
        return Price

    async def get(self, entity_id: str) -> Optional[Price]:
        original = await super().get(entity_id)
        if original is None:
            return None
        original.recurring = PriceRecurring(**original.recurring)
        original.tiers = [PriceTier(**tier) for tier in original.tiers]
        return original
