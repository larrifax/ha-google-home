"""Home Assistant integration for Google Home API."""

from __future__ import annotations

import logging
from typing import Any

import aiohttp

from google_home_api import Device, DeviceState


logger = logging.getLogger(__name__)


class HomeAssistantIntegration:
    """Integration with Home Assistant API."""
    
    def __init__(self) -> None:
        """Initialize the Home Assistant integration."""
        self._session: aiohttp.ClientSession | None = None
        self._ha_url = "http://supervisor/core"
        self._ha_token: str | None = None
        self._initialized = False
        self._devices: dict[str, Device] = {}
    
    async def initialize(self) -> None:
        """Initialize the integration."""
        if self._initialized:
            return
        
        # Get Supervisor token from environment
        import os
        self._ha_token = os.getenv("SUPERVISOR_TOKEN")
        
        if not self._ha_token:
            logger.warning("SUPERVISOR_TOKEN not found, running in standalone mode")
        
        # Create HTTP session
        self._session = aiohttp.ClientSession()
        
        self._initialized = True
        logger.info("Home Assistant integration initialized")
    
    async def close(self) -> None:
        """Close the integration and cleanup resources."""
        if self._session:
            await self._session.close()
            self._session = None
        self._initialized = False
        logger.info("Home Assistant integration closed")
    
    async def _call_api(
        self,
        method: str,
        endpoint: str,
        data: dict[str, Any] | None = None,
    ) -> dict[str, Any] | None:
        """Call the Home Assistant API.
        
        Args:
            method: HTTP method
            endpoint: API endpoint
            data: Request data
            
        Returns:
            Response data or None if request fails
        """
        if not self._session or not self._ha_token:
            logger.debug("Home Assistant API not available")
            return None
        
        url = f"{self._ha_url}/api/{endpoint}"
        headers = {
            "Authorization": f"Bearer {self._ha_token}",
            "Content-Type": "application/json",
        }
        
        try:
            async with self._session.request(
                method, url, json=data, headers=headers
            ) as response:
                if response.status >= 400:
                    logger.warning(f"API call failed: {method} {endpoint}: {response.status}")
                    return None
                
                if response.content_type == "application/json":
                    return await response.json()
                return None
                
        except Exception as e:
            logger.debug(f"API call error: {method} {endpoint}: {e}")
            return None
    
    async def sync_devices(self, devices: list[Device]) -> None:
        """Sync devices to Home Assistant.
        
        This creates or updates device entities in Home Assistant.
        
        Args:
            devices: List of devices to sync
        """
        logger.info(f"Syncing {len(devices)} device(s) to Home Assistant")
        
        # Update internal device cache
        for device in devices:
            self._devices[device.device_id] = device
            logger.debug(f"Synced device: {device.name} ({device.device_id})")
        
        # In a real implementation, this would create/update entities
        # via Home Assistant's device registry and entity registry APIs
        # For now, we'll log the devices
        
        for device in devices:
            logger.info(
                f"Device: {device.name} | Type: {device.device_type} | "
                f"Room: {device.room} | Traits: {', '.join(device.traits)}"
            )
    
    async def update_device_state(
        self,
        device_id: str,
        state: DeviceState,
    ) -> None:
        """Update device state in Home Assistant.
        
        Args:
            device_id: Device identifier
            state: New device state
        """
        device = self._devices.get(device_id)
        if not device:
            logger.warning(f"Unknown device: {device_id}")
            return
        
        logger.debug(
            f"Updating state for {device.name}: "
            f"online={state.online}, attributes={state.attributes}"
        )
        
        # In a real implementation, this would update entity states
        # via Home Assistant's state machine
        
        # Log state changes
        if not state.online:
            logger.warning(f"Device {device.name} is offline")
    
    async def send_command(
        self,
        device_id: str,
        command: str,
        params: dict[str, Any] | None = None,
    ) -> bool:
        """Send a command to a device via Google Home API.
        
        Args:
            device_id: Device identifier
            command: Command to execute
            params: Command parameters
            
        Returns:
            True if command was successful
        """
        device = self._devices.get(device_id)
        if not device:
            logger.warning(f"Unknown device: {device_id}")
            return False
        
        logger.info(f"Sending command to {device.name}: {command} with params {params}")
        
        # In a real implementation, this would be handled by the main loop
        # or a command queue
        return True
