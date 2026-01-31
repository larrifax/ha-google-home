# Google Home API for Home Assistant

[![Home Assistant Add-on](https://img.shields.io/badge/Home%20Assistant-Add--on-blue.svg)](https://www.home-assistant.io/)
[![HACS](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/hacs/integration)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Quality Scale](https://img.shields.io/badge/quality-platinum-purple.svg)](PLATINUM_REQUIREMENTS.md)

A Home Assistant integration that connects with the Google Home API to discover and control smart home devices accessible through Google Home.

**Available as both a HACS Custom Integration and a Home Assistant Add-on.**

## About

This integration enables Home Assistant to communicate with devices exposed via the Google Home API. It provides:

- **Automatic device discovery** from your Google Home ecosystem
- **Real-time state monitoring** of all connected devices
- **Secure OAuth2 authentication** with Google Cloud
- **Easy UI-based configuration** - No YAML editing required (HACS version)
- **Multi-architecture support** for all Home Assistant platforms
- **Automatic error recovery** and connection management
- **Configurable polling intervals** to balance updates and API usage

## Quick Start

Get started in 5 minutes! See the [Quick Start Guide](QUICKSTART.md).

## Installation

### Option 1: HACS (Recommended for Most Users)

**HACS allows you to install this integration on any Home Assistant installation type.**

1. Ensure [HACS](https://hacs.xyz/) is installed in your Home Assistant instance
2. In Home Assistant, go to **HACS** → **Integrations**
3. Click the three dots in the top right corner
4. Select **Custom repositories**
5. Add repository URL: `https://github.com/larrifax/ha-google-home`
6. Select category: **Integration**
7. Click **Add**
8. Find "Google Home API" in the integration list
9. Click **Download**
10. Restart Home Assistant
11. Go to **Settings** → **Devices & Services** → **Add Integration**
12. Search for "Google Home API"
13. Enter your Google Cloud credentials in the configuration dialog
14. Click **Submit**

### Option 2: Home Assistant Add-on (Supervised/OS Only)

**The Add-on approach is only available for Home Assistant OS and Supervised installations.**

1. Navigate to the Home Assistant Add-on Store
2. Add this repository URL: `https://github.com/larrifax/ha-google-home`
3. Find "Google Home API" in the add-on list
4. Click "Install"
5. Configure the add-on with your credentials (see Configuration section below)
6. Start the add-on

## Configuration

### Prerequisites

Before using this integration, you need to set up Google Cloud credentials:

1. Create a Google Cloud project
2. Enable the Home Graph API
3. Create OAuth2 credentials
4. Obtain a refresh token

See the [complete documentation](google_home/DOCS.md) for detailed setup instructions.

### HACS Integration Configuration

When using the HACS integration, configuration is done through the Home Assistant UI:

1. Go to **Settings** → **Devices & Services**
2. Click **Add Integration** and search for "Google Home API"
3. Enter your credentials in the configuration dialog:
   - **Google Cloud Project ID**
   - **OAuth2 Client ID**
   - **OAuth2 Client Secret**
   - **OAuth2 Refresh Token**
4. (Optional) After setup, click **Configure** to adjust:
   - **Scan Interval**: Seconds between device updates (default: 30)

### Add-on Configuration

When using the Add-on approach, configure via YAML:

#### Required Configuration

```yaml
project_id: "your-project-id"
client_id: "your-client-id.apps.googleusercontent.com"
client_secret: "your-client-secret"
refresh_token: "your-refresh-token"
```

#### Optional Configuration

```yaml
log_level: "info"  # debug, info, warning, or error
scan_interval: 30  # seconds between updates (10-300)
```

## Features

- ✅ Device discovery from Google Home
- ✅ State monitoring and updates
- ✅ OAuth2 authentication
- ✅ Automatic token refresh
- ✅ Error handling and recovery
- ✅ Multi-architecture support
- ✅ Configurable logging
- ✅ AppArmor security profile
- ✅ Health monitoring
- ✅ Comprehensive documentation

## Quality Scale

This integration aims to achieve the **Platinum** level on the Home Assistant Quality Scale by following best practices:

- **Strict typing** with Pydantic models
- **Comprehensive error handling** and automatic recovery
- **Full documentation** with setup guides and troubleshooting
- **Security** with secure credential handling and OAuth2
- **Performance** with configurable polling and efficient API usage
- **Maintainability** with clean code and type checking
- **UI Configuration Flow** for easy setup (HACS version)

See [Platinum Requirements](PLATINUM_REQUIREMENTS.md) for detailed compliance information.

## Documentation

- 🚀 [Quick Start Guide](QUICKSTART.md) - Get started in 5 minutes
- 📖 [Complete Documentation](google_home/DOCS.md) - Setup and usage guide
- 🏆 [Platinum Requirements](PLATINUM_REQUIREMENTS.md) - Quality scale compliance
- 📝 [Changelog](google_home/CHANGELOG.md) - Version history
- 👨‍💻 [Development Guide](DEVELOPMENT.md) - For contributors
- 🤝 [Contributing Guide](CONTRIBUTING.md) - How to contribute
- 🌍 [Translations](google_home/translations/) - Localization files

## Support

- **Issues**: [GitHub Issues](https://github.com/larrifax/ha-google-home/issues)
- **Discussions**: [GitHub Discussions](https://github.com/larrifax/ha-google-home/discussions)
- **Home Assistant Community**: Tag with `google-home-api`

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes with tests
4. Submit a pull request

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

## License

MIT License - See [LICENSE](LICENSE) file for details

## Credits

Built for the Home Assistant community with ❤️

Designed to meet the [Platinum Quality Scale](https://www.home-assistant.io/docs/quality_scale/) requirements.
