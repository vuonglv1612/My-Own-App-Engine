from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from .tables.base import custom_json_serializer


def create_session_factory(postgres_uri):
    engine = create_async_engine(postgres_uri, json_serializer=custom_json_serializer)
    session_factory = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    return session_factory


def create_sync_session_factory(postgres_uri):
    engine = create_engine(postgres_uri, json_serializer=custom_json_serializer)
    session_factory = sessionmaker(engine, expire_on_commit=False)
    return session_factory
