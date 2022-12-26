from typing import Optional

from src.services.provisioner import Provisioner


class FakeProvisioner(Provisioner):
    def __init__(self):
        self._data = {}

    async def create_app(self, project_id: str, app_name: str, plan: str, description: Optional[str] = None) -> None:
        self._data[app_name] = {
            "project_id": project_id,
            "plan": plan,
            "app_name": app_name,
            "description": description,
        }

    def get_app(self, app_name: str):
        return self._data.get(app_name)

    def delete_app(self, app_name: str):
        self._data.pop(app_name, None)
