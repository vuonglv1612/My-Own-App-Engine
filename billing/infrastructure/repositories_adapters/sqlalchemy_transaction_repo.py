from typing import Optional, Type

from core.interfaces.repositories import TransactionRepository
from core.models import Transaction
from sqlalchemy import select
from utils import paging

from .repository import SqlalchemyRepository


class SqlalchemyTransactionRepository(TransactionRepository, SqlalchemyRepository[Transaction]):
    @property
    def entity(self) -> Type[Transaction]:
        return Transaction

    async def list_transaction(self, account_id: str, page: int, page_size: int) -> Optional[Transaction]:
        query = select(Transaction).where(Transaction.account_id == account_id)
        query = paging.paginate(query, page, page_size)
        result = await self._session.execute(query)
        return result.all()
