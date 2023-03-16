import redis
from celery import Celery

from config import settings


def celery_app_factory():
    celery = Celery(
        "worker",
        broker=settings.celery_broker_url,
    )
    return celery


def create_redis_client():
    return redis.Redis.from_url(settings.redis_url)
