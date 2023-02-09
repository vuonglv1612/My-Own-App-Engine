from typing import Optional, Type

from core.interfaces.repositories import SubscriptionItemRepository
from core.models import SubscriptionItem
from .repository import SqlalchemyRepository


class SqlalchemySubscriptionItemRepository(SubscriptionItemRepository, SqlalchemyRepository[SubscriptionItem]):
    @property
    def entity(self) -> Type[SubscriptionItem]:
        return SubscriptionItem

    async def get(self, entity_id: str) -> Optional[SubscriptionItem]:
        original = await super().get(entity_id)
        if original is None:
            return None
        return original
