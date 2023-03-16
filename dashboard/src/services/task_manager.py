from abc import ABC, abstractmethod

from celery import Celery


class TaskManager(ABC):
    @abstractmethod
    async def send_task(self, task, params):
        raise NotImplementedError


class CeleryTaskManager(TaskManager):
    def __init__(self, celery_app: Celery):
        self._celery_app = celery_app

    async def send_task(self, task, params):
        return self._celery_app.send_task(task, kwargs=params)
