"""Constants for the Google Home API integration."""

from __future__ import annotations

DOMAIN = "google_home"

# Configuration keys
CONF_PROJECT_ID = "project_id"
CONF_CLIENT_ID = "client_id"
CONF_CLIENT_SECRET = "client_secret"
CONF_REFRESH_TOKEN = "refresh_token"

# Default values
DEFAULT_SCAN_INTERVAL = 30

# Google API URLs
GOOGLE_OAUTH_TOKEN_URI = "https://oauth2.googleapis.com/token"
GOOGLE_HOME_API_BASE_URL = "https://homegraph.googleapis.com/v1"

# Device types
DEVICE_TYPE_LIGHT = "LIGHT"
DEVICE_TYPE_SWITCH = "SWITCH"
DEVICE_TYPE_OUTLET = "OUTLET"
DEVICE_TYPE_THERMOSTAT = "THERMOSTAT"
DEVICE_TYPE_SENSOR = "SENSOR"

# Attributes
ATTR_DEVICE_ID = "device_id"
ATTR_DEVICE_TYPE = "device_type"
ATTR_ROOM = "room"
ATTR_MANUFACTURER = "manufacturer"
ATTR_MODEL = "model"
ATTR_HW_VERSION = "hw_version"
ATTR_SW_VERSION = "sw_version"
ATTR_TRAITS = "traits"
