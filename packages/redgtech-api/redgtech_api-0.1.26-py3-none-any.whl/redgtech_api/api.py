import aiohttp
import logging

_LOGGER = logging.getLogger(__name__)

API_URL = "https://redgtech.com"

class RedgtechAuthError(Exception):
    """Raised when authentication fails."""

class RedgtechConnectionError(Exception):
    """Raised when there is a connection issue."""

class RedgtechAPI:
    def __init__(self, token=None):
        self._token = token

    async def login(self, email: str, password: str) -> str:
        """Authenticate with the Redgtech API and retrieve an access token."""
        async with aiohttp.ClientSession() as session:
            url = f"{API_URL}/home_assistant/login"
            try:
                async with session.post(url, json={'email': email, 'password': password}) as response:
                    if response.status == 401:
                        raise RedgtechAuthError("Invalid email or password")
                    response.raise_for_status()
                    data = await response.json()
                    self._token = data.get('data', {}).get('access_token')
                    if not self._token:
                        raise RedgtechAuthError("No access token received from API")
                    return self._token
            except aiohttp.ClientError as e:
                _LOGGER.error("Connection error during login: %s", e)
                raise RedgtechConnectionError("Failed to connect to Redgtech API") from e
            except Exception as e:
                _LOGGER.error("Unexpected error during login: %s", e)
                raise RedgtechConnectionError("Unexpected error during login") from e

    async def get_data(self, token: str = None) -> dict:
        """Fetch data from the Redgtech API."""
        token = token or self._token
        if not token:
            raise RedgtechAuthError("No access token available for fetching data")
        async with aiohttp.ClientSession() as session:
            url = f"{API_URL}/home_assistant?access_token={token}"
            try:
                async with session.get(url) as response:
                    response.raise_for_status()
                    return await response.json()
            except aiohttp.ClientError as e:
                _LOGGER.error("Connection error while fetching data: %s", e)
                raise RedgtechConnectionError("Failed to connect to Redgtech API") from e
            except Exception as e:
                _LOGGER.error("Unexpected error while fetching data: %s", e)
                raise RedgtechConnectionError("Unexpected error while fetching data") from e

    async def set_switch_state(self, endpoint_id: str, state: bool, token: str = None) -> bool:
        """Set the state of a switch."""
        token = token or self._token
        if not token:
            raise RedgtechAuthError("No access token available for setting switch state")
        try:
            id_part, after_id = endpoint_id.split("-", 1)
            number_channel = ''.join(filter(str.isdigit, after_id))
            type_channel = ''.join(filter(str.isalpha, after_id))
            state_char = 'l' if state else 'd'
            value = f"{number_channel}{state_char}" if type_channel == "AC" else f"{type_channel}{number_channel}*{state_char}*"
            url = f"{API_URL}/home_assistant/execute/{id_part}?cod=?{value}"
            headers = {"Authorization": f"{token}"}
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=headers) as response:
                    response.raise_for_status()
                    return response.status == 200
        except aiohttp.ClientError as e:
            _LOGGER.error("Connection error while setting switch state: %s", e)
            raise RedgtechConnectionError("Failed to connect to Redgtech API") from e
        except Exception as e:
            _LOGGER.error("Unexpected error while setting switch state: %s", e)
            raise

    async def set_light_brightness(self, endpoint_id: str, brightness: int, token: str = None) -> bool:
        """Set the brightness of a light."""
        token = token or self._token
        if not token:
            raise RedgtechAuthError("No access token available for setting light brightness")
        try:
            id_part, after_id = endpoint_id.split("-", 1)
            number_channel = ''.join(char for char in after_id if char.isdigit())
            type_channel = ''.join(char for char in after_id if char.isalpha())
            brightness_value = round((brightness / 255) * 100)
            value = f"{type_channel}{number_channel}*{brightness_value}*"
            url = f"{API_URL}/home_assistant/execute/{id_part}?cod=?{value}"
            headers = {"Authorization": f"{token}"}
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=headers) as response:
                    response.raise_for_status()
                    return response.status == 200
        except aiohttp.ClientError as e:
            _LOGGER.error("Connection error while setting light brightness: %s", e)
            raise RedgtechConnectionError("Failed to connect to Redgtech API") from e
        except Exception as e:
            _LOGGER.error("Unexpected error while setting light brightness: %s", e)
            raise RedgtechConnectionError("Unexpected error while setting light brightness") from e