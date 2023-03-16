import asyncio
import json
import os
import time

import aiohttp
import jwt

from src.utils.retry import async_retry_decorator


class TokenError(Exception):
    pass


def set_up():
    """Sets up configuration for the app"""
    config = {
        "DOMAIN": os.getenv("DOMAIN", "your.domain.com"),
        "API_AUDIENCE": os.getenv("API_AUDIENCE", "your.audience.com"),
        "ISSUER": os.getenv("ISSUER", "https://your.domain.com/"),
        "ALGORITHMS": os.getenv("ALGORITHMS", "RS256"),
    }
    return config


class VerifyToken():
    """Does all the token verification using PyJWT"""

    def __init__(self, token, permissions=None, scopes=None):
        self.token = token
        self.permissions = permissions
        self.scopes = scopes
        self.config = set_up()

        # This gets the JWKS from a given URL and does processing so you can use any of
        # the keys available
        jwks_url = f'https://{self.config["DOMAIN"]}/.well-known/jwks.json'
        self.jwks_client = jwt.PyJWKClient(jwks_url)

    def verify(self):
        # This gets the 'kid' from the passed token
        try:
            self.signing_key = self.jwks_client.get_signing_key_from_jwt(
                self.token
            ).key
        except jwt.exceptions.PyJWKClientError as error:
            return {"status": "error", "msg": error.__str__()}
        except jwt.exceptions.DecodeError as error:
            return {"status": "error", "msg": error.__str__()}

        try:
            payload = jwt.decode(
                self.token,
                self.signing_key,
                algorithms=self.config["ALGORITHMS"],
                audience=self.config["API_AUDIENCE"],
                # issuer=self.config["ISSUER"],
            )
        except Exception as e:
            return {"status": "error", "message": str(e)}
        return payload


async def get_user_info(redis_client, sub, token):
    """Gets the user info from Auth0"""

    @async_retry_decorator(retries=3, delay=1)
    async def _call_api():
        url = "https://appengine.jp.auth0.com/userinfo"
        payload = {}
        headers = {
            "Authorization": f"Bearer {token}"
        }
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers, data=payload) as response:
                if not response.ok:
                    if response.status == 409:
                        reset_timestamp = response.headers.get("x-ratelimit-reset")
                        if reset_timestamp:
                            remaining = int(reset_timestamp) - int(time.time())
                            await asyncio.sleep(remaining)
                    raise ValueError(await response.text())
                raw = await response.text()
                try:
                    data = json.loads(raw)
                except json.decoder.JSONDecodeError:
                    raise ValueError("Invalid response from Auth0 API")
                return data

    user_info = await redis_client.get(f"auth0_user_info_{sub}")
    if user_info:
        print("User info from cache")
        return json.loads(user_info)
    else:
        data = await _call_api()
        await redis_client.set(f"auth0_user_info_{sub}", json.dumps(data))
        print("User info from API")
        return data
