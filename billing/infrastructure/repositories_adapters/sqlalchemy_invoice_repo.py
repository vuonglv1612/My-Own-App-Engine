from typing import Type, Optional

from sqlalchemy import select

from core.interfaces.repositories import InvoiceRepository
from core.models import Invoice
from .repository import SqlalchemyRepository
from utils import paging


class SqlalchemyInvoiceRepository(InvoiceRepository, SqlalchemyRepository[Invoice]):
    @property
    def entity(self) -> Type[Invoice]:
        return Invoice

    async def get_by_status(self, account_id, status: str, page: int, page_size: int) -> Optional[Invoice]:
        query = select(Invoice)
        if not status:
            query = query.where(Invoice.account_id == account_id)
            query = paging.paginate(query, page, page_size)
            result = await self._session.execute(query)
        else:
            query = query.where(Invoice.status == status, Invoice.account_id == account_id)
            query = paging.paginate(query, page, page_size)
            result = await self._session.execute(query)
        return result.all()
