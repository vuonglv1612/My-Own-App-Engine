import pytest

from .fakes.unit_of_work import UnitOfWorkFactory


@pytest.fixture
def uow_factory():
    return UnitOfWorkFactory()
