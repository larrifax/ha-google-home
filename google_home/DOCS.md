# Google Home API Add-on Documentation

## About

The Google Home API add-on enables Home Assistant to communicate with and control devices that are available through the Google Home ecosystem. This add-on discovers devices, monitors their states, and allows control of smart home devices connected to your Google Home.

## Features

- **Device Discovery**: Automatically discovers all devices accessible through Google Home
- **State Monitoring**: Continuously monitors device states and reports changes
- **Multi-Architecture Support**: Works on all Home Assistant supported architectures
- **Secure Authentication**: Uses OAuth2 for secure API access
- **Automatic Recovery**: Handles connection failures and automatically recovers
- **Configurable Polling**: Adjustable scan interval to balance freshness and API usage
- **Comprehensive Logging**: Detailed logging with configurable verbosity
- **Type Safety**: Strict type checking for reliability

## Prerequisites

Before using this add-on, you need:

1. A Google Cloud Platform account
2. A Google Cloud project with the Home Graph API enabled
3. OAuth2 credentials configured for your project
4. A refresh token obtained through the OAuth2 flow

## Setup Instructions

### Step 1: Create a Google Cloud Project

1. Go to the [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Note your Project ID (you'll need this later)

### Step 2: Enable the Home Graph API

1. In your Google Cloud project, navigate to "APIs & Services" > "Library"
2. Search for "Home Graph API"
3. Click on it and enable it for your project

### Step 3: Create OAuth2 Credentials

1. Go to "APIs & Services" > "Credentials"
2. Click "Create Credentials" > "OAuth 2.0 Client ID"
3. Select "Web application" as the application type
4. Add authorized redirect URIs (e.g., `http://localhost:8080/callback`)
5. Click "Create" and save the Client ID and Client Secret

### Step 4: Obtain a Refresh Token

You need to perform an OAuth2 authorization flow to get a refresh token:

1. Use the OAuth2 playground or create a simple authorization script
2. Request authorization with the following scope:
   - `https://www.googleapis.com/auth/homegraph`
3. Complete the authorization flow to obtain a refresh token

Example using Python:

```python
from google_auth_oauthlib.flow import InstalledAppFlow

# Create the flow using the client secrets file
flow = InstalledAppFlow.from_client_config(
    {
        "installed": {
            "client_id": "YOUR_CLIENT_ID",
            "client_secret": "YOUR_CLIENT_SECRET",
            "redirect_uris": ["http://localhost:8080/callback"],
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token"
        }
    },
    scopes=['https://www.googleapis.com/auth/homegraph']
)

# Run the flow and get credentials
credentials = flow.run_local_server(port=8080)

# Print the refresh token
print(f"Refresh token: {credentials.refresh_token}")
```

### Step 5: Configure the Add-on

1. Install this add-on in Home Assistant
2. Go to the add-on configuration page
3. Fill in the following fields:
   - **Project ID**: Your Google Cloud Project ID
   - **Client ID**: OAuth2 Client ID from Step 3
   - **Client Secret**: OAuth2 Client Secret from Step 3
   - **Refresh Token**: The refresh token from Step 4
   - **Log Level**: Choose your preferred logging level (default: info)
   - **Scan Interval**: How often to poll for updates in seconds (default: 30)

### Step 6: Start the Add-on

1. Save the configuration
2. Start the add-on
3. Check the logs to verify it's working correctly

## Configuration

### Required Configuration

- **project_id** (string): Your Google Cloud Project ID
- **client_id** (string): OAuth2 Client ID
- **client_secret** (string): OAuth2 Client Secret
- **refresh_token** (string): OAuth2 Refresh Token

### Optional Configuration

- **log_level** (string): Logging verbosity level
  - `debug`: Detailed debugging information
  - `info`: General informational messages (default)
  - `warning`: Warning messages only
  - `error`: Error messages only

- **scan_interval** (integer): Seconds between device state updates
  - Minimum: 10 seconds
  - Maximum: 300 seconds (5 minutes)
  - Default: 30 seconds
  - Recommendation: 30-60 seconds for most use cases

## How It Works

1. **Initialization**: The add-on starts and validates your configuration
2. **Authentication**: Uses your refresh token to obtain an access token
3. **Discovery**: Calls the Google Home API to discover all available devices
4. **Synchronization**: Creates or updates device information in Home Assistant
5. **Monitoring**: Continuously polls device states at the configured interval
6. **Updates**: Reports state changes to Home Assistant
7. **Recovery**: Automatically handles errors and reconnects if needed

## Device Support

This add-on supports all device types available through the Google Home API, including:

- **Lights**: On/off, brightness, color control
- **Switches**: On/off control
- **Outlets**: On/off control
- **Thermostats**: Temperature control, mode settings
- **Locks**: Lock/unlock control
- **Cameras**: Device status
- **Sensors**: Various sensor types
- **And more**: Any device type supported by Google Home

Device capabilities depend on the traits supported by each device.

## Troubleshooting

### Add-on won't start

**Problem**: The add-on fails to start or immediately stops.

**Solutions**:
1. Check the add-on logs for error messages
2. Verify all required configuration fields are filled in
3. Ensure your OAuth2 credentials are correct
4. Verify the Home Graph API is enabled in your Google Cloud project

### No devices discovered

**Problem**: The add-on starts but doesn't find any devices.

**Solutions**:
1. Verify you have devices set up in Google Home
2. Check that your refresh token has the correct scope (`homegraph`)
3. Ensure your Google Cloud project has access to your Google Home devices
4. Check the add-on logs for API errors

### Authentication errors

**Problem**: Error messages about authentication or token refresh.

**Solutions**:
1. Verify your Client ID and Client Secret are correct
2. Ensure your refresh token is valid and hasn't been revoked
3. Check that your Google Cloud project is active
4. Try generating a new refresh token

### Devices not updating

**Problem**: Device states in Home Assistant don't match actual device states.

**Solutions**:
1. Check the scan interval - increase frequency for faster updates
2. Verify network connectivity to Google's servers
3. Check for rate limiting in the add-on logs
4. Ensure devices are online in the Google Home app

### High API usage

**Problem**: Concerned about API quotas or costs.

**Solutions**:
1. Increase the scan interval to reduce polling frequency
2. Review Google Cloud quota limits for the Home Graph API
3. Monitor your API usage in the Google Cloud Console
4. Consider whether you need real-time updates or if longer intervals are acceptable

## Logging

The add-on provides detailed logging to help troubleshoot issues:

- **debug**: Very detailed information including API requests and responses
- **info**: General operational information
- **warning**: Important notices that don't prevent operation
- **error**: Problems that prevent proper functioning

To enable debug logging:
1. Go to the add-on configuration
2. Set "Log Level" to "debug"
3. Restart the add-on
4. Check the logs for detailed information

## Security

### Best Practices

1. **Keep credentials secure**: Never share your Client Secret or Refresh Token
2. **Use AppArmor**: The add-on includes an AppArmor profile for enhanced security
3. **Regular updates**: Keep the add-on updated to get security fixes
4. **Limit scope**: Only grant the minimum necessary API scopes
5. **Monitor access**: Regularly review OAuth2 access in your Google Account

### Data Privacy

- The add-on only communicates with Google's servers and your Home Assistant instance
- Credentials are stored securely in Home Assistant's configuration
- No data is sent to third parties
- All API communication uses HTTPS encryption

## Performance

### Resource Usage

The add-on is designed to be lightweight:
- **CPU**: Minimal usage during polling cycles
- **Memory**: Typically 30-50 MB depending on device count
- **Network**: Proportional to scan frequency and device count

### Scaling

The add-on can handle:
- 100+ devices with default settings
- Configurable scan intervals to optimize performance
- Automatic rate limiting to prevent API quota issues

## API Limits

Google Home API has usage limits:
- Check your Google Cloud Console for specific quotas
- Default limits are typically sufficient for home use
- The add-on includes automatic retry logic for rate limits
- Adjust scan interval if approaching limits

## Support

For issues and feature requests:
- GitHub Issues: https://github.com/larrifax/ha-google-home/issues
- Home Assistant Community: Tag your post with `google-home-api`

## License

This add-on is provided as-is without warranty. See the LICENSE file for details.

## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## Credits

Built for the Home Assistant community with the goal of achieving Platinum quality scale.

## Version History

See [CHANGELOG.md](CHANGELOG.md) for detailed version history.
