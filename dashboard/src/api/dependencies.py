from src.services.unit_of_work import MemoryUnitOfWork


def unit_of_work():
    """Provide a unit of work."""
    # TODO: Use a factory to create the unit of work.
    # session_factory = None
    # uow = SQLAlchemyUnitOfWork(session_factory=session_factory)
    uow = MemoryUnitOfWork()
    return uow
