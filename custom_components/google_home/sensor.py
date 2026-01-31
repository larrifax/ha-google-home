"""Sensor platform for Google Home API integration."""

from __future__ import annotations

import logging
from datetime import timedelta
from typing import Any

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
    UpdateFailed,
)

from .api import Device, GoogleHomeAPI
from .const import (
    ATTR_DEVICE_ID,
    ATTR_DEVICE_TYPE,
    ATTR_HW_VERSION,
    ATTR_MANUFACTURER,
    ATTR_MODEL,
    ATTR_ROOM,
    ATTR_SW_VERSION,
    ATTR_TRAITS,
    DEFAULT_SCAN_INTERVAL,
    DOMAIN,
)

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Google Home API sensors from a config entry."""
    data = hass.data[DOMAIN][entry.entry_id]
    api: GoogleHomeAPI = data["api"]

    # Create coordinator for updating device data
    coordinator = GoogleHomeDataUpdateCoordinator(hass, api)

    # Fetch initial data
    await coordinator.async_config_entry_first_refresh()

    # Create sensors for discovered devices
    entities = []
    for device in coordinator.data:
        entities.append(GoogleHomeDeviceSensor(coordinator, device, entry))

    async_add_entities(entities, True)


class GoogleHomeDataUpdateCoordinator(DataUpdateCoordinator[list[Device]]):
    """Class to manage fetching Google Home device data."""

    def __init__(self, hass: HomeAssistant, api: GoogleHomeAPI) -> None:
        """Initialize the coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=DEFAULT_SCAN_INTERVAL),
        )
        self.api = api

    async def _async_update_data(self) -> list[Device]:
        """Fetch data from Google Home API."""
        try:
            devices = await self.api.discover_devices()
            _LOGGER.debug("Discovered %d devices", len(devices))

            # Query state for all devices
            for device in devices:
                try:
                    state = await self.api.query_device_state(device.device_id)
                    # Store state in device for later use
                    device.state = state
                except Exception as err:
                    _LOGGER.warning(
                        "Failed to query state for device %s: %s",
                        device.device_id,
                        err,
                    )

            return devices
        except Exception as err:
            raise UpdateFailed(f"Error communicating with API: {err}") from err


class GoogleHomeDeviceSensor(
    CoordinatorEntity[GoogleHomeDataUpdateCoordinator], SensorEntity
):
    """Representation of a Google Home device sensor."""

    def __init__(
        self,
        coordinator: GoogleHomeDataUpdateCoordinator,
        device: Device,
        entry: ConfigEntry,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._device = device
        self._entry = entry
        self._attr_unique_id = f"{DOMAIN}_{device.device_id}"
        self._attr_name = device.name

    @property
    def device_info(self) -> DeviceInfo:
        """Return device information."""
        return DeviceInfo(
            identifiers={(DOMAIN, self._device.device_id)},
            name=self._device.name,
            manufacturer=self._device.manufacturer or "Unknown",
            model=self._device.model or "Unknown",
            hw_version=self._device.hw_version,
            sw_version=self._device.sw_version,
            via_device=(DOMAIN, self.coordinator.api.project_id),
        )

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return extra state attributes."""
        return {
            ATTR_DEVICE_ID: self._device.device_id,
            ATTR_DEVICE_TYPE: self._device.device_type,
            ATTR_ROOM: self._device.room,
            ATTR_MANUFACTURER: self._device.manufacturer,
            ATTR_MODEL: self._device.model,
            ATTR_HW_VERSION: self._device.hw_version,
            ATTR_SW_VERSION: self._device.sw_version,
            ATTR_TRAITS: self._device.traits,
        }

    @property
    def native_value(self) -> str:
        """Return the state of the sensor."""
        # Find updated device data from coordinator
        for device in self.coordinator.data:
            if device.device_id == self._device.device_id:
                self._device = device
                # Check if device has state attribute (set in coordinator)
                if hasattr(device, "state"):
                    return "online" if device.state.online else "offline"
                break
        return "unknown"
