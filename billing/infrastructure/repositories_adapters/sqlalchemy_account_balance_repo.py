from typing import Type, Optional

from sqlalchemy import select

from core.interfaces.repositories import AccountBalanceRepository
from core.models import AccountBalance
from .repository import SqlalchemyRepository


class SqlalchemyAccountBalanceRepository(AccountBalanceRepository, SqlalchemyRepository[AccountBalance]):
    @property
    def entity(self) -> Type[AccountBalance]:
        return AccountBalance

    async def get_by_account_id(self, account_id: str) -> Optional[AccountBalance]:
        query = select(AccountBalance).where(AccountBalance.account_id == account_id)
        result = await self._session.execute(query)
        return result.scalars().first()
