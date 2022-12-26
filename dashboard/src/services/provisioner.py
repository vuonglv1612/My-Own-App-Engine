from abc import ABC, abstractmethod
from typing import Optional


class Provisioner(ABC):
    @abstractmethod
    async def create_app(self, project_id: str, app_name: str, plan: str, description: Optional[str] = None) -> None:
        pass


class TsuruProvisioner(Provisioner):
    def __init__(self, tsuru_api_url: str, tsuru_token: str):
        self._tsuru_api_url = tsuru_api_url
        self._tsuru_token = tsuru_token

    async def create_app(self, project_id: str, app_name: str, plan: str, description: Optional[str] = None) -> None:
        # TODO: implement this
        pass
