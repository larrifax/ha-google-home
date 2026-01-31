# Google Home API Integration

Integrate Home Assistant with devices accessible through the Google Home API.

## Features

- **Automatic device discovery** - Find all devices connected through Google Home
- **Real-time state monitoring** - Monitor device states and attributes
- **OAuth2 secure authentication** - Secure connection to Google Cloud
- **Easy UI-based configuration** - No YAML editing required
- **Configurable polling interval** - Balance between updates and API usage

## Prerequisites

Before installing this integration, you need:

1. **Google Cloud Platform account**
2. **Google Cloud project** with Home Graph API enabled
3. **OAuth2 credentials** (Client ID and Client Secret)
4. **OAuth2 refresh token** obtained through the authorization flow

## Installation via HACS

1. Open HACS in Home Assistant
2. Go to "Integrations"
3. Click the three dots in the top right
4. Select "Custom repositories"
5. Add this repository URL: `https://github.com/larrifax/ha-google-home`
6. Select "Integration" as the category
7. Click "Add"
8. Find "Google Home API" in the HACS integration list
9. Click "Download"
10. Restart Home Assistant

## Configuration

After installation:

1. Go to **Settings** → **Devices & Services**
2. Click **+ Add Integration**
3. Search for "Google Home API"
4. Enter your Google Cloud credentials:
   - Google Cloud Project ID
   - OAuth2 Client ID
   - OAuth2 Client Secret
   - OAuth2 Refresh Token
5. Click **Submit**

The integration will discover your devices and create sensor entities for each one.

## Options

After setup, you can configure additional options:

- **Scan Interval**: How often to poll for device updates (default: 30 seconds)

## Support

- **Issues**: [GitHub Issues](https://github.com/larrifax/ha-google-home/issues)
- **Documentation**: [Complete Guide](https://github.com/larrifax/ha-google-home)
