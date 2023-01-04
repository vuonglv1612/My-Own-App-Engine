from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import registry
from sqlalchemy.orm import sessionmaker

from config import settings
from src.core import entities
from src.infrastructure.postgres import models


def start_mappers():
    mapper_registry = registry(metadata=models.metadata)
    mapper_registry.map_imperatively(entities.App, models.AppTable, version_id_col=models.AppTable.c.version_number)
    mapper_registry.map_imperatively(entities.Plan, models.PlanTable)
    mapper_registry.map_imperatively(
        entities.Project, models.ProjectTable, version_id_col=models.ProjectTable.c.version_number
    )


def create_session_factory():
    engine = create_async_engine(settings.async_postgresql_uri)
    session_factory = sessionmaker(engine, class_=AsyncSession)
    return session_factory
