"""The Google Home API integration."""

from __future__ import annotations

import logging
from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers import device_registry as dr

from .api import GoogleHomeAPI
from .const import (
    CONF_CLIENT_ID,
    CONF_CLIENT_SECRET,
    CONF_PROJECT_ID,
    CONF_REFRESH_TOKEN,
    DOMAIN,
)

_LOGGER = logging.getLogger(__name__)

PLATFORMS: list[Platform] = [Platform.SENSOR]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Google Home API from a config entry."""
    _LOGGER.debug("Setting up Google Home API integration")

    # Extract configuration
    project_id = entry.data[CONF_PROJECT_ID]
    client_id = entry.data[CONF_CLIENT_ID]
    client_secret = entry.data[CONF_CLIENT_SECRET]
    refresh_token = entry.data[CONF_REFRESH_TOKEN]

    # Initialize API client
    api = GoogleHomeAPI(
        project_id=project_id,
        client_id=client_id,
        client_secret=client_secret,
        refresh_token=refresh_token,
    )

    try:
        await api.initialize()
    except Exception as e:
        _LOGGER.error("Failed to initialize Google Home API: %s", e)
        return False

    # Store API client in hass.data
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = {
        "api": api,
        "devices": {},
    }

    # Register the integration device
    device_registry = dr.async_get(hass)
    device_registry.async_get_or_create(
        config_entry_id=entry.entry_id,
        identifiers={(DOMAIN, project_id)},
        name="Google Home API",
        manufacturer="Google",
        model="Google Home API",
    )

    # Forward setup to platforms
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    _LOGGER.info("Google Home API integration setup complete")
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    _LOGGER.debug("Unloading Google Home API integration")

    # Unload platforms
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)

    if unload_ok:
        # Close API client
        data = hass.data[DOMAIN].pop(entry.entry_id)
        api: GoogleHomeAPI = data["api"]
        await api.close()

    return unload_ok


async def async_reload_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Reload config entry."""
    await async_unload_entry(hass, entry)
    await async_setup_entry(hass, entry)
