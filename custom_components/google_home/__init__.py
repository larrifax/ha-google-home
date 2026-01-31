"""The Google Home API integration."""

from __future__ import annotations

import logging
from datetime import timedelta

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import (
    CONF_CLIENT_ID,
    CONF_CLIENT_SECRET,
    CONF_PROJECT_ID,
    CONF_REFRESH_TOKEN,
    CONF_SCAN_INTERVAL,
    DEFAULT_SCAN_INTERVAL,
    DOMAIN,
)
from .google_home_api import GoogleHomeAPI

_LOGGER = logging.getLogger(__name__)

PLATFORMS: list[Platform] = [Platform.SENSOR]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Google Home API from a config entry."""
    _LOGGER.debug("Setting up Google Home API integration")

    # Get configuration
    project_id = entry.data[CONF_PROJECT_ID]
    client_id = entry.data[CONF_CLIENT_ID]
    client_secret = entry.data[CONF_CLIENT_SECRET]
    refresh_token = entry.data[CONF_REFRESH_TOKEN]
    scan_interval = entry.options.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL)

    # Initialize Google Home API client
    api = GoogleHomeAPI(
        project_id=project_id,
        client_id=client_id,
        client_secret=client_secret,
        refresh_token=refresh_token,
    )

    try:
        await api.initialize()
    except Exception as err:
        _LOGGER.error("Failed to initialize Google Home API: %s", err)
        return False

    async def async_update_data():
        """Fetch data from Google Home API."""
        try:
            devices = await api.discover_devices()

            # Query state for each device
            device_states = {}
            for device in devices:
                try:
                    state = await api.query_device_state(device.device_id)
                    device_states[device.device_id] = {
                        "device": device,
                        "state": state,
                    }
                except Exception as err:
                    _LOGGER.warning(
                        "Failed to query state for device %s: %s",
                        device.device_id,
                        err,
                    )
                    # Include device even if state query fails
                    device_states[device.device_id] = {
                        "device": device,
                        "state": None,
                    }

            return device_states
        except Exception as err:
            raise UpdateFailed(f"Error communicating with API: {err}") from err

    # Create update coordinator
    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name=DOMAIN,
        update_method=async_update_data,
        update_interval=timedelta(seconds=scan_interval),
    )

    # Fetch initial data
    await coordinator.async_config_entry_first_refresh()

    # Store coordinator and API client
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = {
        "coordinator": coordinator,
        "api": api,
    }

    # Set up platforms
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    # Register update listener for options
    entry.async_on_unload(entry.add_update_listener(async_reload_entry))

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
        api = data["api"]
        await api.close()

    return unload_ok


async def async_reload_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Reload config entry when options change."""
    await hass.config_entries.async_reload(entry.entry_id)
