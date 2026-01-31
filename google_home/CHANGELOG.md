# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-01-31

### Added
- Initial release of Google Home API add-on
- Google Home API integration for device discovery
- Device state querying and updates
- OAuth2 authentication support
- Multi-architecture support (aarch64, amd64, armhf, armv7, i386)
- Comprehensive error handling and automatic recovery
- Configurable scan interval for device polling
- Strict type checking with Pydantic models
- Health check monitoring
- AppArmor security profile
- Comprehensive logging with configurable log levels
- Internationalization support (English)
- Home Assistant supervisor integration
- Automatic token refresh mechanism
- Device caching and state management

### Features
- Discovers all devices available through Google Home
- Syncs device information to Home Assistant
- Polls device states at configurable intervals
- Supports device control commands (prepared for future implementation)
- Automatic error recovery and retry logic
- Secure credential management
- Full documentation and setup guide

### Security
- AppArmor profile for container isolation
- Secure OAuth2 token management
- No hardcoded credentials
- Minimal container privileges
