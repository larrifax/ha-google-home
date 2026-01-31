"""Google Home API client implementation."""

from __future__ import annotations

import asyncio
import logging
from typing import Any

import aiohttp
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)


class Device(BaseModel):
    """Represents a Google Home device."""

    device_id: str = Field(..., description="Unique device identifier")
    name: str = Field(..., description="Device name")
    device_type: str = Field(..., description="Device type (e.g., LIGHT, SWITCH)")
    traits: list[str] = Field(default_factory=list, description="Device capabilities")
    room: str | None = Field(None, description="Room assignment")
    manufacturer: str | None = Field(None, description="Device manufacturer")
    model: str | None = Field(None, description="Device model")
    hw_version: str | None = Field(None, description="Hardware version")
    sw_version: str | None = Field(None, description="Software version")


class DeviceState(BaseModel):
    """Represents device state."""

    online: bool = Field(default=True, description="Device online status")
    attributes: dict[str, Any] = Field(
        default_factory=dict, description="Device state attributes"
    )


class GoogleHomeAPI:
    """Client for interacting with Google Home API."""

    BASE_URL = "https://homegraph.googleapis.com/v1"

    def __init__(
        self,
        project_id: str,
        client_id: str,
        client_secret: str,
        refresh_token: str,
    ) -> None:
        """Initialize the Google Home API client.

        Args:
            project_id: Google Cloud project ID
            client_id: OAuth2 client ID
            client_secret: OAuth2 client secret
            refresh_token: OAuth2 refresh token
        """
        self.project_id = project_id
        self._credentials = Credentials(
            token=None,
            refresh_token=refresh_token,
            client_id=client_id,
            client_secret=client_secret,
            token_uri="https://oauth2.googleapis.com/token",
        )
        self._session: aiohttp.ClientSession | None = None
        self._initialized = False

    async def initialize(self) -> None:
        """Initialize the API client."""
        if self._initialized:
            return

        # Create HTTP session
        self._session = aiohttp.ClientSession()

        # Refresh access token
        await self._refresh_token()

        self._initialized = True
        logger.info("Google Home API client initialized")

    async def close(self) -> None:
        """Close the API client and cleanup resources."""
        if self._session:
            await self._session.close()
            self._session = None
        self._initialized = False
        logger.info("Google Home API client closed")

    async def _refresh_token(self) -> None:
        """Refresh the OAuth2 access token."""
        try:
            # Run blocking refresh call in executor to avoid blocking the event loop
            request = Request()
            loop = asyncio.get_event_loop()
            await loop.run_in_executor(None, self._credentials.refresh, request)
            logger.debug("Access token refreshed successfully")
        except Exception as e:
            logger.error(f"Failed to refresh access token: {e}")
            raise

    async def _make_request(
        self,
        method: str,
        endpoint: str,
        data: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Make an authenticated request to the Google Home API.

        Args:
            method: HTTP method (GET, POST, etc.)
            endpoint: API endpoint path
            data: Request payload (for POST requests)

        Returns:
            Response data as dictionary

        Raises:
            Exception: If the request fails
        """
        if not self._session:
            raise RuntimeError("API client not initialized")

        # Ensure token is valid
        if not self._credentials.valid:
            await self._refresh_token()

        url = f"{self.BASE_URL}/{endpoint}"
        headers = {
            "Authorization": f"Bearer {self._credentials.token}",
            "Content-Type": "application/json",
        }

        try:
            async with self._session.request(
                method, url, json=data, headers=headers
            ) as response:
                response.raise_for_status()
                return await response.json()
        except aiohttp.ClientError as e:
            logger.error(f"Request failed: {method} {url}: {e}")
            raise

    async def discover_devices(self) -> list[Device]:
        """Discover all devices available through Google Home.

        Returns:
            List of discovered devices
        """
        try:
            # Request device sync to get all devices
            data = {
                "agentUserId": self.project_id,
                "requestId": "discover-request",
            }

            response = await self._make_request("POST", "devices:sync", data)

            # Parse devices from response
            devices = []
            payload = response.get("payload", {})

            for device_data in payload.get("devices", []):
                try:
                    device = Device(
                        device_id=device_data.get("id", ""),
                        name=device_data.get("name", {}).get("name", "Unknown"),
                        device_type=device_data.get("type", "UNKNOWN"),
                        traits=list(device_data.get("traits", [])),
                        room=device_data.get("roomHint", None),
                        manufacturer=device_data.get("deviceInfo", {}).get(
                            "manufacturer", None
                        ),
                        model=device_data.get("deviceInfo", {}).get("model", None),
                        hw_version=device_data.get("deviceInfo", {}).get(
                            "hwVersion", None
                        ),
                        sw_version=device_data.get("deviceInfo", {}).get(
                            "swVersion", None
                        ),
                    )
                    devices.append(device)
                except Exception as e:
                    logger.warning(f"Failed to parse device: {e}")
                    continue

            logger.info(f"Discovered {len(devices)} device(s)")
            return devices

        except Exception as e:
            logger.error(f"Failed to discover devices: {e}")
            raise

    async def query_device_state(self, device_id: str) -> DeviceState:
        """Query the current state of a device.

        Args:
            device_id: Device identifier

        Returns:
            Current device state
        """
        try:
            data = {
                "agentUserId": self.project_id,
                "requestId": f"query-{device_id}",
                "inputs": [
                    {
                        "intent": "action.devices.QUERY",
                        "payload": {"devices": [{"id": device_id}]},
                    }
                ],
            }

            response = await self._make_request("POST", "devices:query", data)

            # Parse state from response
            payload = response.get("payload", {})
            device_states = payload.get("devices", {})
            device_state_data = device_states.get(device_id, {})

            return DeviceState(
                online=device_state_data.get("online", False),
                attributes=device_state_data,
            )

        except Exception as e:
            logger.error(f"Failed to query device state for {device_id}: {e}")
            raise

    async def execute_command(
        self,
        device_id: str,
        command: str,
        params: dict[str, Any] | None = None,
    ) -> bool:
        """Execute a command on a device.

        Args:
            device_id: Device identifier
            command: Command to execute (e.g., action.devices.commands.OnOff)
            params: Command parameters

        Returns:
            True if command was successful
        """
        try:
            data = {
                "agentUserId": self.project_id,
                "requestId": f"execute-{device_id}",
                "inputs": [
                    {
                        "intent": "action.devices.EXECUTE",
                        "payload": {
                            "commands": [
                                {
                                    "devices": [{"id": device_id}],
                                    "execution": [
                                        {"command": command, "params": params or {}}
                                    ],
                                }
                            ]
                        },
                    }
                ],
            }

            response = await self._make_request("POST", "devices:execute", data)

            # Check command status
            payload = response.get("payload", {})
            commands = payload.get("commands", [])

            if commands:
                status = commands[0].get("status", "ERROR")
                success = status == "SUCCESS"

                if not success:
                    logger.warning(f"Command failed for {device_id}: {status}")

                return success

            return False

        except Exception as e:
            logger.error(f"Failed to execute command for {device_id}: {e}")
            return False
