#!/usr/bin/env python3
"""
Google Home API Integration for Home Assistant.

This add-on integrates with the Google Home API to discover and control
smart home devices that are available through Google Home.
"""

from __future__ import annotations

import asyncio
import logging
import os
import sys

from google_home_api import GoogleHomeAPI
from ha_integration import HomeAssistantIntegration


def setup_logging() -> logging.Logger:
    """Set up logging configuration."""
    log_level = os.getenv("LOG_LEVEL", "INFO").upper()

    # Configure root logger
    logging.basicConfig(
        level=getattr(logging, log_level, logging.INFO),
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        stream=sys.stdout,
    )

    return logging.getLogger(__name__)


async def main() -> None:
    """Run the main application loop."""
    logger = setup_logging()
    logger.info("Google Home API Add-on starting...")

    # Get configuration from environment
    project_id = os.getenv("PROJECT_ID")
    client_id = os.getenv("CLIENT_ID")
    client_secret = os.getenv("CLIENT_SECRET")
    refresh_token = os.getenv("REFRESH_TOKEN")
    scan_interval = int(os.getenv("SCAN_INTERVAL", "30"))

    # Validate configuration
    if not all([project_id, client_id, client_secret, refresh_token]):
        logger.error("Missing required configuration")
        sys.exit(1)

    logger.info(f"Project ID: {project_id}")
    logger.info(f"Scan interval: {scan_interval} seconds")

    # Initialize Google Home API client
    try:
        google_api = GoogleHomeAPI(
            project_id=project_id,
            client_id=client_id,
            client_secret=client_secret,
            refresh_token=refresh_token,
        )
        await google_api.initialize()
        logger.info("Google Home API client initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize Google Home API: {e}")
        sys.exit(1)

    # Initialize Home Assistant integration
    try:
        ha_integration = HomeAssistantIntegration()
        await ha_integration.initialize()
        logger.info("Home Assistant integration initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize Home Assistant integration: {e}")
        sys.exit(1)

    # Main loop
    logger.info("Starting main loop...")
    try:
        while True:
            try:
                # Discover and sync devices
                logger.debug("Discovering devices...")
                devices = await google_api.discover_devices()
                logger.info(f"Found {len(devices)} device(s)")

                # Sync devices to Home Assistant
                await ha_integration.sync_devices(devices)

                # Query device states
                logger.debug("Querying device states...")
                for device in devices:
                    try:
                        state = await google_api.query_device_state(device.device_id)
                        await ha_integration.update_device_state(
                            device.device_id, state
                        )
                    except Exception as e:
                        logger.warning(
                            f"Failed to query state for device {device.device_id}: {e}"
                        )

            except Exception as e:
                logger.error(f"Error in main loop: {e}", exc_info=True)
                logger.info("Retrying in 60 seconds...")
                await asyncio.sleep(60)
                continue

            # Wait for next scan interval
            await asyncio.sleep(scan_interval)

    except KeyboardInterrupt:
        logger.info("Shutting down...")
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        sys.exit(1)
    finally:
        # Cleanup
        try:
            await google_api.close()
            await ha_integration.close()
        except Exception as e:
            logger.error(f"Error during cleanup: {e}")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nShutting down...")
        sys.exit(0)
    except Exception as e:
        print(f"Fatal error: {e}")
        sys.exit(1)
