from typing import Type

from core.interfaces.repositories import SubscriptionRepository
from core.models import Subscription
from .repository import SqlalchemyRepository


class SqlalchemySubscriptionRepository(SubscriptionRepository, SqlalchemyRepository[Subscription]):
    @property
    def entity(self) -> Type[Subscription]:
        return Subscription
