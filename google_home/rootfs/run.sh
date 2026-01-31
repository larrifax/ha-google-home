#!/usr/bin/env bashio
set -e

# ==============================================================================
# Google Home API Add-on
# Starts the Google Home API integration service
# ==============================================================================

bashio::log.info "Starting Google Home API add-on..."

# Parse configuration
CONFIG_PATH=/data/options.json

export PROJECT_ID=$(bashio::config 'project_id')
export CLIENT_ID=$(bashio::config 'client_id')
export CLIENT_SECRET=$(bashio::config 'client_secret')
export REFRESH_TOKEN=$(bashio::config 'refresh_token')
export LOG_LEVEL=$(bashio::config 'log_level')
export SCAN_INTERVAL=$(bashio::config 'scan_interval')

# Validate required configuration
if [ -z "$PROJECT_ID" ]; then
    bashio::log.fatal "Project ID is required. Please configure the add-on."
    exit 1
fi

if [ -z "$CLIENT_ID" ]; then
    bashio::log.fatal "Client ID is required. Please configure the add-on."
    exit 1
fi

if [ -z "$CLIENT_SECRET" ]; then
    bashio::log.fatal "Client Secret is required. Please configure the add-on."
    exit 1
fi

if [ -z "$REFRESH_TOKEN" ]; then
    bashio::log.fatal "Refresh Token is required. Please configure the add-on."
    exit 1
fi

# Set default values
export LOG_LEVEL=${LOG_LEVEL:-info}
export SCAN_INTERVAL=${SCAN_INTERVAL:-30}

bashio::log.info "Configuration validated successfully"
bashio::log.info "Log level: ${LOG_LEVEL}"
bashio::log.info "Scan interval: ${SCAN_INTERVAL} seconds"

# Start the Python application
bashio::log.info "Starting Google Home API service..."
cd /app
exec python3 /app/main.py
