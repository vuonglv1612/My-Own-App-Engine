from tests.fake.fake_provisioner import FakeProvisioner
from tests.fake.fake_unit_of_work import MemoryUnitOfWork


class FakeUnitOfWorkFactory:
    @staticmethod
    def for_test_create_app():
        return MemoryUnitOfWork()


class FakeProvisionerFactory:
    @staticmethod
    def for_test_create_app():
        return FakeProvisioner()
