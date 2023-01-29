from typing import Type

from core.interfaces.repositories import AccountRepository
from core.models import Account
from .repository import SqlalchemyRepository


class SqlalchemyAccountRepository(AccountRepository, SqlalchemyRepository[Account]):
    @property
    def entity(self) -> Type[Account]:
        return Account
