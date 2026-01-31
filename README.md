# Google Home API Add-on for Home Assistant

[![Home Assistant Add-on](https://img.shields.io/badge/Home%20Assistant-Add--on-blue.svg)](https://www.home-assistant.io/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

A Home Assistant add-on that integrates with the Google Home API to discover and control smart home devices accessible through Google Home.

## About

This add-on enables Home Assistant to communicate with devices exposed via the Google Home API. It provides:

- **Automatic device discovery** from your Google Home ecosystem
- **Real-time state monitoring** of all connected devices
- **Secure OAuth2 authentication** with Google Cloud
- **Multi-architecture support** for all Home Assistant platforms
- **Automatic error recovery** and connection management
- **Configurable polling intervals** to balance updates and API usage

## Installation

1. Navigate to the Home Assistant Add-on Store
2. Add this repository URL: `https://github.com/larrifax/ha-google-home`
3. Find "Google Home API" in the add-on list
4. Click "Install"
5. Configure the add-on (see Configuration section)
6. Start the add-on

## Configuration

Before using this add-on, you need to set up Google Cloud credentials:

1. Create a Google Cloud project
2. Enable the Home Graph API
3. Create OAuth2 credentials
4. Obtain a refresh token

See the [complete documentation](google_home/DOCS.md) for detailed setup instructions.

### Required Configuration

```yaml
project_id: "your-project-id"
client_id: "your-client-id.apps.googleusercontent.com"
client_secret: "your-client-secret"
refresh_token: "your-refresh-token"
```

### Optional Configuration

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

This add-on aims to achieve the **Platinum** level on the Home Assistant Quality Scale by following best practices:

- **Strict typing** with Pydantic models
- **Comprehensive error handling** and automatic recovery
- **Full documentation** with setup guides and troubleshooting
- **Security** with AppArmor profiles and secure credential handling
- **Performance** with configurable polling and efficient API usage
- **Maintainability** with clean code and type checking

## Documentation

- [Complete Documentation](google_home/DOCS.md) - Setup and usage guide
- [Changelog](google_home/CHANGELOG.md) - Version history
- [Translations](google_home/translations/) - Localization files

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

## License

MIT License - See [LICENSE](LICENSE) file for details

## Credits

Built for the Home Assistant community with ❤️
