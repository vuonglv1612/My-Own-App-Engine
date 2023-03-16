from src.dependencies import billing_client_factory, provisioner_factory, deploy_client_factory
from src.dependencies import create_session_factory, redis_client_factory
from src.services.unit_of_work import SQLAlchemyUnitOfWork


async def unit_of_work():
    """Provide a unit of work."""
    session_factory = create_session_factory()
    uow = SQLAlchemyUnitOfWork(session_factory=session_factory)
    return uow


async def get_billing_client():
    """Provide a billing client."""
    return billing_client_factory()


async def get_provisioner():
    """Provide a provisioner."""
    return provisioner_factory()


async def get_deploy_client():
    """Provide a deploy client."""
    return deploy_client_factory()


async def get_redis_client():
    """Provide a redis client."""
    return redis_client_factory()
