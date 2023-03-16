import aiohttp


class DeployClient:
    def __init__(self, api_url: str):
        self._api_url = api_url

    async def deploy_git_app(self, deployment_id: str, app_name: str, git_url: str, git_branch: str, plan_name: str,
                             replicas: int = 1) -> None:
        url = self._api_url + "/deploy-git"
        body = {
            "deployment_id": deployment_id,
            "app_name": app_name,
            "git_url": git_url,
            "git_branch": git_branch,
            "plan_name": plan_name,
            "replicas": replicas,
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=body) as response:
                if response.status != 200:
                    raise ValueError(await response.text())

    async def deploy_image_app(self, deployment_id: str, app_name: str, image: str, plan_name: str,
                               replicas: int = 1) -> None:
        url = self._api_url + "/deploy-image"
        body = {
            "deployment_id": deployment_id,
            "app_name": app_name,
            "image": image,
            "plan_name": plan_name,
            "replicas": replicas,
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=body) as response:
                if response.status != 200:
                    raise ValueError(await response.text())

    async def scale_app(self, app_name: str, change: int) -> None:
        url = self._api_url + "/scale"
        body = {
            "app_name": app_name,
            "change": change,
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=body) as response:
                if response.status != 200:
                    raise ValueError(await response.text())

    async def stop_app(self, app_name: str) -> None:
        url = self._api_url + "/stop"
        body = {
            "app_name": app_name,
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=body) as response:
                if response.status != 200:
                    raise ValueError(await response.text())

    async def restart_app(self, app_name: str) -> None:
        url = self._api_url + "/restart"
        body = {
            "app_name": app_name,
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=body) as response:
                if response.status != 200:
                    raise ValueError(await response.text())
