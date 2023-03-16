from dependencies import celery_app_factory
from task_manager import CeleryTaskManager


def get_task_manager():
    celery_app = celery_app_factory()
    return CeleryTaskManager(celery_app)
