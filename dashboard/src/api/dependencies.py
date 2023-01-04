from src.dependencies import create_session_factory
from src.services.provisioner import TsuruProvisioner
from src.services.unit_of_work import SQLAlchemyUnitOfWork


async def unit_of_work():
    """Provide a unit of work."""
    session_factory = create_session_factory()
    uow = SQLAlchemyUnitOfWork(session_factory=session_factory)
    return uow


async def get_provisioner():
    """Provide a provisioner."""
    # TODO: Use a factory to create the provisioner.
    tsuru_url = "http://tsuru:8080"
    tsuru_token = "token"
    return TsuruProvisioner(tsuru_api_url=tsuru_url, tsuru_token=tsuru_token)
