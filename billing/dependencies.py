from config import settings
from infrastructure.postgres.connection import create_session_factory
from infrastructure.postgres.mapping import start_mapping
from infrastructure.services.unit_of_work import SqlalchemyUnitOfWork

session_factory = create_session_factory(settings.async_postgresql_uri)
start_mapping()


def unit_of_work_factory():
    return SqlalchemyUnitOfWork(session_factory)
