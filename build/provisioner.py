import json

import requests


class TsuruProvisioner:

    def __init__(self, tsuru_api_url: str, username: str, password: str):
        self._tsuru_api_url = tsuru_api_url.strip("/")
        self._username = username
        self._password = password
        self._token = None

    def _login(self, renew: bool = False) -> str:
        if self._token and not renew:
            return self._token
        url = self._tsuru_api_url + "/auth/login"

        payload = f'email={self._username}&password={self._password}'
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        self._token = response.json()["token"]
        return self._token

    def deploy_app(self, app_name: str, image: str):
        token = self._login()
        url = f"{self._tsuru_api_url}/apps/{app_name}/deploy"

        payload = json.dumps({
            "image": f"{image}",
        })
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }
        response = requests.request("POST", url, headers=headers, data=payload, stream=True)
        for line in response.iter_lines():
            yield line.decode('utf-8')

    def scale_up_app(self, app_name: str, up: int):
        token = self._login()
        url = f"{self._tsuru_api_url}/apps/{app_name}/units"

        payload = json.dumps({
            "units": f"{up}",
        })
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }
        response = requests.request("PUT", url, headers=headers, data=payload, stream=True)
        for line in response.iter_lines():
            yield line.decode('utf-8')

    def scale_down_app(self, app_name: str, down: int):
        token = self._login()
        url = f"{self._tsuru_api_url}/apps/{app_name}/units"

        payload = json.dumps({
            "units": f"{down}",
        })
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }
        response = requests.request("DELETE", url, headers=headers, data=payload, stream=True)
        for line in response.iter_lines():
            yield line.decode('utf-8')

    def stop_app(self, app_name):
        token = self._login()
        url = f"{self._tsuru_api_url}/apps/{app_name}/stop"

        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, stream=True)
        for line in response.iter_lines():
            yield line.decode('utf-8')

    def restart_app(self, app_name):
        token = self._login()
        url = f"{self._tsuru_api_url}/apps/{app_name}/restart"

        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }
        response = requests.request("POST", url, headers=headers, stream=True)
        for line in response.iter_lines():
            yield line.decode('utf-8')
