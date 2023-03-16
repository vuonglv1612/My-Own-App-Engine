from abc import ABC, abstractmethod

from src.repositories.activity import ActivityRepository, SQLAlchemyActivityRepository
from src.repositories.app import AppRepository, SQLAlchemyAppRepository
from src.repositories.deployment import DeploymentRepository, SQLAlchemyDeploymentRepository
from src.repositories.environment import EnvironmentRepository, SQLAlchemyEnvironmentRepository
from src.repositories.project import ProjectRepository, SQLAlchemyProjectRepository
from src.repositories.project_member import ProjectMemberRepository, SQLAlchemyProjectMemberRepository
from src.repositories.scale import ScaleRepository, SQLAlchemyScaleRepository
from src.repositories.unit import UnitRepository, SQLAlchemyUnitRepository
from src.repositories.user import UserRepository, SQLAlchemyUserRepository


class UnitOfWork(ABC):
    apps: AppRepository
    projects: ProjectRepository
    project_members: ProjectMemberRepository
    users: UserRepository
    activities: ActivityRepository
    deployments: DeploymentRepository
    environments: EnvironmentRepository
    units: UnitRepository
    scales: ScaleRepository

    async def __aenter__(self):
        await self._connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.rollback()
        await self._disconnect()

    @abstractmethod
    async def _connect(self):
        pass

    @abstractmethod
    async def _disconnect(self):
        pass

    @abstractmethod
    async def rollback(self):
        pass

    @abstractmethod
    async def commit(self):
        pass


class SQLAlchemyUnitOfWork(UnitOfWork):
    def __init__(self, session_factory):
        self._session_factory = session_factory

    async def _connect(self):
        self._session = self._session_factory()
        self.apps = SQLAlchemyAppRepository(self._session)
        self.projects = SQLAlchemyProjectRepository(self._session)
        self.project_members = SQLAlchemyProjectMemberRepository(self._session)
        self.users = SQLAlchemyUserRepository(self._session)
        self.activities = SQLAlchemyActivityRepository(self._session)
        self.deployments = SQLAlchemyDeploymentRepository(self._session)
        self.environments = SQLAlchemyEnvironmentRepository(self._session)
        self.units = SQLAlchemyUnitRepository(self._session)
        self.scales = SQLAlchemyScaleRepository(self._session)

    async def _disconnect(self):
        await self._session.close()

    async def rollback(self):
        await self._session.rollback()

    async def commit(self):
        await self._session.commit()
