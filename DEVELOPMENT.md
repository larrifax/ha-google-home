# Development Guide

This guide helps developers set up and work on the Google Home API add-on.

## Architecture Overview

The add-on consists of three main components:

1. **Google Home API Client** (`google_home_api.py`)
   - Handles OAuth2 authentication
   - Communicates with Google Home Graph API
   - Provides device discovery and control

2. **Home Assistant Integration** (`ha_integration.py`)
   - Bridges between Google Home API and Home Assistant
   - Manages device entities
   - Handles state updates

3. **Main Application** (`main.py`)
   - Orchestrates the integration
   - Manages polling loop
   - Handles error recovery

## Development Environment Setup

### Prerequisites

- Python 3.12 or higher
- Docker and Docker Buildx
- Git
- A text editor or IDE (VS Code recommended)

### Initial Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/larrifax/ha-google-home.git
   cd ha-google-home
   ```

2. **Create a virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r google_home/requirements.txt
   ```

4. **Install development tools:**
   ```bash
   pip install black ruff mypy pytest pytest-asyncio
   ```

## Code Style

We follow these conventions:

- **PEP 8** for Python code style
- **Black** for code formatting (line length: 88)
- **Ruff** for linting
- **Type hints** for all function parameters and return values
- **Docstrings** for all public classes and functions

### Running Code Quality Tools

```bash
# Format code
black google_home/rootfs/app/

# Lint code
ruff check google_home/rootfs/app/

# Type checking
mypy google_home/rootfs/app/

# Check syntax
python3 -m py_compile google_home/rootfs/app/*.py
```

## Project Structure

```
ha-google-home/
├── .github/
│   ├── ISSUE_TEMPLATE/
│   ├── workflows/
│   └── pull_request_template.md
├── google_home/
│   ├── rootfs/
│   │   ├── app/
│   │   │   ├── google_home_api.py    # Google API client
│   │   │   ├── ha_integration.py     # HA integration
│   │   │   └── main.py               # Main application
│   │   └── run.sh                    # Entry point script
│   ├── translations/
│   │   └── en.yaml                   # English translations
│   ├── apparmor.txt                  # Security profile
│   ├── build.yaml                    # Multi-arch build config
│   ├── CHANGELOG.md                  # Version history
│   ├── config.yaml                   # Add-on configuration
│   ├── DOCS.md                       # User documentation
│   ├── Dockerfile                    # Container definition
│   ├── README.md                     # Add-on readme
│   └── requirements.txt              # Python dependencies
├── CONTRIBUTING.md                   # Contribution guidelines
├── LICENSE                           # MIT license
├── README.md                         # Project readme
└── repository.json                   # Add-on repository config
```

## Building the Add-on

### Build Docker Image

```bash
cd google_home
docker build -t google-home-api:dev .
```

### Build for Multiple Architectures

```bash
# Build for amd64
docker buildx build --platform linux/amd64 \
  --build-arg BUILD_FROM=ghcr.io/home-assistant/amd64-base-python:3.12-alpine3.19 \
  -t google-home-api:amd64 .

# Build for aarch64
docker buildx build --platform linux/arm64 \
  --build-arg BUILD_FROM=ghcr.io/home-assistant/aarch64-base-python:3.12-alpine3.19 \
  -t google-home-api:aarch64 .
```

## Testing

### Unit Testing

Create test files in `google_home/tests/`:

```python
import pytest
from google_home_api import GoogleHomeAPI, Device

def test_device_creation():
    device = Device(
        device_id="test-123",
        name="Test Light",
        device_type="LIGHT",
        traits=["OnOff", "Brightness"]
    )
    assert device.device_id == "test-123"
    assert device.name == "Test Light"
```

Run tests:
```bash
pytest google_home/tests/
```

### Integration Testing

Test with a local Home Assistant instance:

1. Copy the add-on to your HA addons directory:
   ```bash
   cp -r google_home /path/to/homeassistant/addons/
   ```

2. Restart Home Assistant

3. Install the add-on from the Supervisor panel

4. Configure with your credentials

5. Check logs for issues

### Manual Testing

```bash
# Test Python syntax
python3 -m py_compile google_home/rootfs/app/*.py

# Test Docker build
docker build -t google-home-api:test google_home/

# Test container startup (will fail without config)
docker run --rm google-home-api:test echo "Container works"
```

## Debugging

### Enable Debug Logging

In the add-on configuration, set:
```yaml
log_level: "debug"
```

### View Logs

- In Home Assistant: Supervisor → Google Home API → Logs
- Or use the command line:
  ```bash
  ha addons logs google_home_api
  ```

### Common Issues

1. **Import errors**: Check that all dependencies are in requirements.txt
2. **Authentication errors**: Verify OAuth2 credentials and token
3. **API errors**: Check Google Cloud project settings and API quotas
4. **Container crashes**: Review logs and check for configuration errors

## Adding New Features

1. **Create a feature branch:**
   ```bash
   git checkout -b feature/my-feature
   ```

2. **Make your changes:**
   - Update Python code
   - Add tests if applicable
   - Update documentation

3. **Test your changes:**
   ```bash
   black google_home/rootfs/app/
   ruff check google_home/rootfs/app/
   python3 -m py_compile google_home/rootfs/app/*.py
   ```

4. **Update documentation:**
   - Update DOCS.md for user-facing changes
   - Update CHANGELOG.md
   - Add code comments

5. **Commit and push:**
   ```bash
   git add .
   git commit -m "Add feature: description"
   git push origin feature/my-feature
   ```

6. **Create a pull request**

## Security Guidelines

1. **Never commit credentials:**
   - Use environment variables
   - Add secrets to .gitignore

2. **Check dependencies:**
   ```bash
   pip list --outdated
   pip-audit  # If installed
   ```

3. **Use security scanning:**
   - GitHub's Dependabot
   - Trivy for container scanning

4. **Follow secure coding practices:**
   - Validate all inputs
   - Use parameterized queries
   - Handle errors properly
   - Log security events

## Documentation

### User Documentation (DOCS.md)

Update when:
- Adding new features
- Changing configuration
- Updating prerequisites
- Adding troubleshooting info

### Code Documentation

- Add docstrings to all public functions
- Use type hints
- Add inline comments for complex logic
- Keep README files up-to-date

### Changelog (CHANGELOG.md)

Follow the format:
```markdown
## [Version] - Date

### Added
- New features

### Changed
- Changes to existing features

### Fixed
- Bug fixes

### Security
- Security updates
```

## Release Process

1. **Update version numbers:**
   - `google_home/config.yaml`
   - `CHANGELOG.md`

2. **Test thoroughly:**
   - Build all architectures
   - Test on Home Assistant
   - Run security scans

3. **Create a release:**
   ```bash
   git tag -a v1.0.0 -m "Release version 1.0.0"
   git push origin v1.0.0
   ```

4. **Update GitHub release:**
   - Add release notes
   - Attach any artifacts

## Resources

- [Home Assistant Add-on Development](https://developers.home-assistant.io/docs/add-ons/)
- [Google Home Graph API](https://developers.home.google.com/reference/home-graph/rest)
- [Python Style Guide (PEP 8)](https://peps.python.org/pep-0008/)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)

## Getting Help

- Open an issue on GitHub
- Check existing documentation
- Review Home Assistant forums
- Ask in the community

## Contributing

See [CONTRIBUTING.md](../CONTRIBUTING.md) for detailed contribution guidelines.
