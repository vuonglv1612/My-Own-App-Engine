from sqlalchemy.orm import registry, relationship

from core import models
from . import tables


def start_mapping():
    mapper_registry = registry(metadata=tables.metadata)
    mapper_registry.map_imperatively(models.Account, tables.AccountTable,
                                     version_id_col=tables.AccountTable.c.version_number)
    mapper_registry.map_imperatively(models.AccountBalance, tables.AccountBalanceTable, properties={
        "transactions": relationship(models.Transaction),
    }, version_id_col=tables.AccountBalanceTable.c.version_number)
    mapper_registry.map_imperatively(models.Transaction, tables.TransactionTable)
