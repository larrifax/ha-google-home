# Google Home API Add-on

Integrate Home Assistant with devices accessible through the Google Home API.

## Installation

Add this repository to your Home Assistant instance:

1. Navigate to **Supervisor** → **Add-on Store** → **⋮** (menu) → **Repositories**
2. Add the repository URL: `https://github.com/larrifax/ha-google-home`
3. Find "Google Home API" in the add-on list
4. Click **Install**

## Configuration

### Prerequisites

You need:
- A Google Cloud Platform account
- A Google Cloud project with Home Graph API enabled
- OAuth2 credentials (Client ID and Secret)
- A refresh token from OAuth2 flow

### Configuration Options

Add-on configuration:

```yaml
project_id: "your-google-cloud-project-id"
client_id: "your-oauth2-client-id.apps.googleusercontent.com"
client_secret: "your-oauth2-client-secret"
refresh_token: "your-oauth2-refresh-token"
log_level: "info"
scan_interval: 30
```

#### Required

- **project_id**: Google Cloud Project ID
- **client_id**: OAuth2 Client ID from Google Cloud Console
- **client_secret**: OAuth2 Client Secret from Google Cloud Console
- **refresh_token**: OAuth2 refresh token for authentication

#### Optional

- **log_level**: Logging level (`debug`, `info`, `warning`, `error`) - default: `info`
- **scan_interval**: Device polling interval in seconds (10-300) - default: `30`

## Documentation

For complete setup instructions, see [DOCS.md](DOCS.md)

## Support

- **Issues**: [GitHub Issues](https://github.com/larrifax/ha-google-home/issues)
- **Documentation**: [Complete Documentation](DOCS.md)
- **Changelog**: [Version History](CHANGELOG.md)
