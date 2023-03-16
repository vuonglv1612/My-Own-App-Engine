import json
from abc import ABC, abstractmethod
from typing import Optional

import aiohttp

from src.utils.retry import async_retry_decorator


class Provisioner(ABC):
    @abstractmethod
    async def create_app(self, app_name: str, plan: str, platform: str, description: Optional[str] = None) -> None:
        pass

    @abstractmethod
    async def delete_app(self, app_name: str) -> None:
        pass

    @abstractmethod
    async def resize_app(self, app_name: str, replicas: int) -> None:
        pass

    @abstractmethod
    async def set_env(self, app_name: str, name: str, value: str) -> None:
        pass

    @abstractmethod
    async def delete_env(self, app_name: str, name: str) -> None:
        pass

    @abstractmethod
    async def add_domain(self, app_name: str, domain: str) -> None:
        pass

    @abstractmethod
    async def remove_domain(self, app_name: str, domain: str) -> None:
        pass


class TsuruProvisioner(Provisioner):

    def __init__(self, tsuru_api_url: str, username: str, password: str):
        self._tsuru_api_url = tsuru_api_url.strip("/")
        self._username = username
        self._password = password
        self._token = None

    async def _login(self, renew: bool = False) -> str:
        if self._token and not renew:
            return self._token
        url = self._tsuru_api_url + "/auth/login"

        payload = f'email={self._username}&password={self._password}'
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(url, data=payload, headers=headers) as response:
                if response.status != 200:
                    raise ValueError(await response.text())
                raw = await response.text()
                try:
                    data = json.loads(raw)
                except json.decoder.JSONDecodeError:
                    raise ValueError("Invalid response from Tsuru API")
                self._token = data["token"]
        return self._token

    async def create_app(self, app_name: str, plan: str, platform: str, description: Optional[str] = None) -> None:
        @async_retry_decorator(retries=3, delay=1)
        async def _create_app():
            await self._login()
            url = self._tsuru_api_url + "/apps"
            payload = json.dumps({
                "name": app_name,
                "plan": plan,
                "pool": "local",
                "platform": "static",
                "description": description or "",
                "teamOwner": "admin",
                "metadata": {}
            })
            headers = {
                'Authorization': f'Bearer {self._token}',
                'Content-Type': 'application/json'
            }
            async with aiohttp.ClientSession() as session:
                async with session.post(url, data=payload, headers=headers) as response:
                    if not response.ok:
                        if response.status == 401:
                            await self._login(renew=True)
                        elif response.status == 409:
                            raise ValueError(f"Ứng dụng {app_name} đã tồn tại")
                        raise ValueError(await response.text())
                    raw = await response.text()
                    try:
                        data = json.loads(raw)
                    except json.decoder.JSONDecodeError:
                        raise ValueError("Invalid response from Tsuru API")
                    return data

        await _create_app()

    async def resize_app(self, app_name: str, replicas: int = 1) -> None:
        @async_retry_decorator(retries=3, delay=1)
        async def _resize_app_retry():
            await self._login()
            url = self._tsuru_api_url + f"/apps/{app_name}/units"
            payload = {
                "units": replicas
            }
            headers = {
                'Authorization': f'Bearer {self._token}',
                'Content-Type': 'application/json'
            }

            async with aiohttp.ClientSession() as session:
                async with session.put(url, data=json.dumps(payload), headers=headers) as response:
                    if not response.ok:
                        if response.status == 401:
                            await self._login(renew=True)
                        raise ValueError(await response.text())
                    raw = await response.text()
                    try:
                        data = json.loads(raw)
                    except json.decoder.JSONDecodeError:
                        raise ValueError("Invalid response from Tsuru API")
                    return data

        return await _resize_app_retry()

    async def delete_app(self, app_name: str) -> None:
        @async_retry_decorator(retries=3, delay=1)
        async def _delete_app_retry():
            await self._login()
            url = self._tsuru_api_url + f"/apps/{app_name}"
            headers = {
                'Authorization': f'Bearer {self._token}',
                'Content-Type': 'application/json'
            }

            async with aiohttp.ClientSession() as session:
                async with session.delete(url, headers=headers) as response:
                    if not response.ok:
                        if response.status == 401:
                            await self._login(renew=True)
                        raise ValueError(await response.text())

        return await _delete_app_retry()

    async def set_env(self, app_name: str, name: str, value: str):
        @async_retry_decorator(retries=3, delay=1)
        async def _set_env_retry():
            await self._login()
            url = self._tsuru_api_url + f"/apps/{app_name}/env"
            payload = {
                "envs": [
                    {
                        "name": name,
                        "value": value
                    }
                ],
                "norestart": True
            }
            headers = {
                'Authorization': f'Bearer {self._token}',
                'Content-Type': 'application/json'
            }

            async with aiohttp.ClientSession() as session:
                async with session.post(url, data=json.dumps(payload), headers=headers) as response:
                    if not response.ok:
                        if response.status == 401:
                            await self._login(renew=True)
                        raise ValueError(await response.text())

        return await _set_env_retry()

    async def delete_env(self, app_name: str, name: str):
        @async_retry_decorator(retries=3, delay=1)
        async def _delete_env_retry():
            await self._login()
            url = self._tsuru_api_url + f"/apps/{app_name}/env?env={name}&norestart=true"
            headers = {
                "Authorization": f"Bearer {self._token}",
                "Content-Type": "application/json"
            }

            async with aiohttp.ClientSession() as session:
                async with session.delete(url, headers=headers) as response:
                    if not response.ok:
                        if response.status == 401:
                            await self._login(renew=True)
                        raise ValueError(await response.text())

        return await _delete_env_retry()

    async def add_domain(self, app_name: str, domain: str):
        @async_retry_decorator(retries=3, delay=1)
        async def _add_domain_retry():
            await self._login()
            url = self._tsuru_api_url + f"/apps/{app_name}/cname"
            payload = {
                "cname": [
                    domain
                ]
            }
            headers = {
                "Authorization": f"Bearer {self._token}",
                "Content-Type": "application/json"
            }

            async with aiohttp.ClientSession() as session:
                async with session.post(url, data=json.dumps(payload), headers=headers) as response:
                    if not response.ok:
                        if response.status == 401:
                            await self._login(renew=True)
                        raise ValueError(await response.text())

        return await _add_domain_retry()

    async def remove_domain(self, app_name: str, domain: str):
        @async_retry_decorator(retries=3, delay=1)
        async def _remove_domain_retry():
            await self._login()
            url = self._tsuru_api_url + f"/apps/{app_name}/cname"
            payload = {
                "cname": [
                    domain
                ]
            }
            headers = {
                "Authorization": f"Bearer {self._token}",
                "Content-Type": "application/json"
            }

            async with aiohttp.ClientSession() as session:
                async with session.delete(url, data=json.dumps(payload), headers=headers) as response:
                    if not response.ok:
                        if response.status == 401:
                            await self._login(renew=True)
                        raise ValueError(await response.text())

        return await _remove_domain_retry()
