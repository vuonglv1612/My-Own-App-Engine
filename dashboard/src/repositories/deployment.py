from abc import ABC

from .base import SQLAlchemyRepository, IRepository
from ..core.entities import Deployment


class DeploymentRepository(IRepository[Deployment], ABC):
    """
    Deployment repository interface.
    """


class SQLAlchemyDeploymentRepository(SQLAlchemyRepository[Deployment], DeploymentRepository):
    @staticmethod
    def _get_model():
        return Deployment
