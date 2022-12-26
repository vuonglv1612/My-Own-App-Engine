import pytest

from tests.fake.factory import FakeUnitOfWorkFactory, FakeProvisionerFactory


@pytest.fixture
def uow_factory():
    return FakeUnitOfWorkFactory()


@pytest.fixture
def provisioner_factory():
    return FakeProvisionerFactory()
