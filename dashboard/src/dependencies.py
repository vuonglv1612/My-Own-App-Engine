from aioredis import Redis
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import registry, relationship
from sqlalchemy.orm import sessionmaker

from config import settings
from src.core import entities
from src.infrastructure.postgres import models
from src.services.billing import BillingClient
from src.services.build_client import DeployClient
from src.services.provisioner import TsuruProvisioner


def start_mappers():
    mapper_registry = registry(metadata=models.metadata)
    mapper_registry.map_imperatively(entities.App, models.AppTable, version_id_col=models.AppTable.c.version_number,
                                     properties={
                                         "activities": relationship(entities.Activity, back_populates="app",
                                                                    cascade="all, delete-orphan"),
                                         "environments": relationship(entities.Environment, back_populates="app",
                                                                      cascade="all, delete-orphan"),
                                         "project": relationship(entities.Project, back_populates="apps"),
                                         "scales": relationship(entities.Scale, back_populates="app",
                                                                cascade="all, delete-orphan")})
    mapper_registry.map_imperatively(
        entities.Project, models.ProjectTable, version_id_col=models.ProjectTable.c.version_number, properties={
            "members": relationship(entities.ProjectMember, back_populates="project", cascade="all, delete-orphan"),
            "apps": relationship(entities.App, back_populates="project", cascade="all, delete-orphan")}
    )
    mapper_registry.map_imperatively(entities.User, models.UserTable)
    mapper_registry.map_imperatively(entities.ProjectMember, models.ProjectMemberTable, properties={
        "project": relationship(entities.Project, back_populates="members"), "user": relationship(entities.User)})
    mapper_registry.map_imperatively(entities.Activity, models.ActivityTable, properties={
        "app": relationship(entities.App)})
    mapper_registry.map_imperatively(entities.Deployment, models.DeploymentTable, properties={
        "app": relationship(entities.App), "scale": relationship(entities.Scale)})
    mapper_registry.map_imperatively(entities.Environment, models.EnvironmentTable, properties={
        "app": relationship(entities.App)})
    mapper_registry.map_imperatively(entities.Unit, models.UnitTable)
    mapper_registry.map_imperatively(entities.Scale, models.ScaleTable, properties={
        "unit": relationship(entities.Unit), "app": relationship(entities.App),
        "deployments": relationship(entities.Deployment, back_populates="scale", cascade="all, delete-orphan")})


def create_session_factory():
    engine = create_async_engine(settings.async_postgresql_uri)
    session_factory = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    return session_factory


def create_sync_session_factory():
    engine = create_engine(settings.postgresql_uri)
    session_factory = sessionmaker(engine, expire_on_commit=False)
    return session_factory


def billing_client_factory():
    return BillingClient(settings.billing_service_url)


def provisioner_factory():
    return TsuruProvisioner(tsuru_api_url=settings.tsuru_api_url, username=settings.tsuru_username,
                            password=settings.tsuru_password)


def deploy_client_factory():
    return DeployClient(settings.deploy_service_url)


def redis_client_factory():
    return Redis.from_url(settings.redis_url)
