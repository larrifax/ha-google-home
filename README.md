# Google Home API Custom Integration for Home Assistant

[![Home Assistant](https://img.shields.io/badge/Home%20Assistant-Integration-blue.svg)](https://www.home-assistant.io/)
[![HACS](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/hacs/integration)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Quality Scale](https://img.shields.io/badge/quality-platinum-purple.svg)](PLATINUM_REQUIREMENTS.md)

A Home Assistant custom integration that integrates with the Google Home API to discover and control smart home devices accessible through Google Home.

## About

This integration enables Home Assistant to communicate with devices exposed via the Google Home API. It provides:

- **Automatic device discovery** from your Google Home ecosystem
- **Real-time state monitoring** of all connected devices
- **Secure OAuth2 authentication** with Google Cloud
- **Multi-architecture support** for all Home Assistant platforms
- **Automatic error recovery** and connection management
- **Configurable polling intervals** to balance updates and API usage

## Quick Start

Get started in 5 minutes! See the [Quick Start Guide](QUICKSTART.md).

## Installation

### HACS (Recommended)

1. Open HACS in your Home Assistant instance
2. Click on "Integrations"
3. Click the three dots in the top right corner
4. Select "Custom repositories"
5. Add this repository URL: `https://github.com/larrifax/ha-google-home`
6. Select "Integration" as the category
7. Click "Add"
8. Find "Google Home API" in the integration list
9. Click "Download"
10. Restart Home Assistant
11. Go to Settings → Devices & Services
12. Click "+ Add Integration"
13. Search for "Google Home API"
14. Follow the configuration steps

### Manual Installation

1. Download the latest release from the [releases page](https://github.com/larrifax/ha-google-home/releases)
2. Extract the `custom_components/google_home` folder to your Home Assistant `custom_components` directory
3. Restart Home Assistant
4. Go to Settings → Devices & Services
5. Click "+ Add Integration"
6. Search for "Google Home API"
7. Follow the configuration steps

## Configuration

Before using this integration, you need to set up Google Cloud credentials:

1. Create a Google Cloud project
2. Enable the Home Graph API
3. Create OAuth2 credentials
4. Obtain a refresh token

See the [complete documentation](google_home/DOCS.md) for detailed setup instructions.

### Setup via Home Assistant UI

After installation, configure the integration through the Home Assistant UI:

1. Go to Settings → Devices & Services
2. Click "+ Add Integration"
3. Search for "Google Home API"
4. Enter your credentials:
   - **Google Cloud Project ID**: Your Google Cloud Project ID
   - **OAuth2 Client ID**: Your OAuth2 Client ID from Google Cloud
   - **OAuth2 Client Secret**: Your OAuth2 Client Secret from Google Cloud
   - **OAuth2 Refresh Token**: Your OAuth2 Refresh Token

The integration will automatically discover your Google Home devices and create entities for them.

## Features

- ✅ Device discovery from Google Home
- ✅ State monitoring and updates
- ✅ OAuth2 authentication
- ✅ Automatic token refresh
- ✅ Error handling and recovery
- ✅ UI-based configuration through Home Assistant
- ✅ Automatic entity creation for discovered devices
- ✅ HACS compatibility
- ✅ Comprehensive documentation

## Quality Scale

This integration aims to achieve the **Platinum** level on the Home Assistant Quality Scale by following best practices:

- **Strict typing** with Pydantic models
- **Comprehensive error handling** and automatic recovery
- **Full documentation** with setup guides and troubleshooting
- **Security** with secure credential handling
- **Performance** with efficient API usage and update coordination
- **Maintainability** with clean code and type checking
- **HACS compatibility** for easy installation and updates

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
