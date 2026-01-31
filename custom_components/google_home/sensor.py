"""Sensor platform for Google Home API integration."""

from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import (
    ATTR_DEVICE_ID,
    ATTR_DEVICE_TYPE,
    ATTR_HW_VERSION,
    ATTR_MANUFACTURER,
    ATTR_MODEL,
    ATTR_ROOM,
    ATTR_SW_VERSION,
    ATTR_TRAITS,
    DOMAIN,
)

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Google Home API sensors from a config entry."""
    coordinator = hass.data[DOMAIN][config_entry.entry_id]["coordinator"]

    # Create sensor entities for each device
    entities = []
    for device_id, device_data in coordinator.data.items():
        device = device_data["device"]
        entities.append(GoogleHomeDeviceSensor(coordinator, device_id, device))

    async_add_entities(entities)


class GoogleHomeDeviceSensor(CoordinatorEntity, SensorEntity):
    """Representation of a Google Home device sensor."""

    def __init__(self, coordinator, device_id: str, device) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._device_id = device_id
        self._device = device
        self._attr_unique_id = f"{DOMAIN}_{device_id}"
        self._attr_name = device.name
        self._attr_has_entity_name = False

    @property
    def device_info(self) -> dict[str, Any]:
        """Return device information about this entity."""
        info = {
            "identifiers": {(DOMAIN, self._device_id)},
            "name": self._device.name,
            "model": self._device.model or "Unknown",
        }

        if self._device.manufacturer:
            info["manufacturer"] = self._device.manufacturer

        if self._device.sw_version:
            info["sw_version"] = self._device.sw_version

        if self._device.hw_version:
            info["hw_version"] = self._device.hw_version

        return info

    @property
    def native_value(self) -> str | None:
        """Return the state of the sensor."""
        device_data = self.coordinator.data.get(self._device_id)
        if not device_data:
            return None

        state = device_data.get("state")
        if state is None:
            return "unavailable"

        return "online" if state.online else "offline"

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return the state attributes."""
        device_data = self.coordinator.data.get(self._device_id)
        if not device_data:
            return {}

        device = device_data["device"]
        state = device_data.get("state")

        attributes = {
            ATTR_DEVICE_ID: self._device_id,
            ATTR_DEVICE_TYPE: device.device_type,
            ATTR_TRAITS: device.traits,
        }

        if device.room:
            attributes[ATTR_ROOM] = device.room

        if device.manufacturer:
            attributes[ATTR_MANUFACTURER] = device.manufacturer

        if device.model:
            attributes[ATTR_MODEL] = device.model

        if device.hw_version:
            attributes[ATTR_HW_VERSION] = device.hw_version

        if device.sw_version:
            attributes[ATTR_SW_VERSION] = device.sw_version

        # Add state attributes if available
        if state and state.attributes:
            attributes.update(state.attributes)

        return attributes

    @property
    def available(self) -> bool:
        """Return True if entity is available."""
        if not self.coordinator.last_update_success:
            return False

        device_data = self.coordinator.data.get(self._device_id)
        return device_data is not None
