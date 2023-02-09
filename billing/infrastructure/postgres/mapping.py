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
    mapper_registry.map_imperatively(models.Product, tables.ProductTable,
                                     version_id_col=tables.ProductTable.c.version_number)
    mapper_registry.map_imperatively(models.Price, tables.PriceTable)
    mapper_registry.map_imperatively(models.Subscription, tables.SubscriptionTable)
    mapper_registry.map_imperatively(models.SubscriptionItem, tables.SubscriptionItemsTable)
    mapper_registry.map_imperatively(models.Invoice, tables.InvoiceTable)
    mapper_registry.map_imperatively(models.InvoiceLine, tables.InvoiceLineTable)
