# Contributing to Google Home API Add-on

Thank you for your interest in contributing! This document provides guidelines for contributing to this project.

## Code of Conduct

Be respectful, inclusive, and constructive in all interactions.

## How to Contribute

### Reporting Issues

When reporting issues, please include:
- Description of the problem
- Steps to reproduce
- Expected behavior
- Actual behavior
- Add-on version
- Home Assistant version
- Logs (with sensitive information removed)

### Suggesting Enhancements

Feature requests are welcome! Please:
- Check if the feature is already requested
- Provide a clear use case
- Explain the expected behavior
- Consider implementation complexity

### Pull Requests

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/your-feature`
3. **Make your changes**:
   - Follow existing code style
   - Add or update tests if applicable
   - Update documentation
   - Ensure no security vulnerabilities
4. **Commit your changes**: Use clear, descriptive commit messages
5. **Push to your fork**: `git push origin feature/your-feature`
6. **Open a pull request**: Provide a clear description of changes

## Development Setup

### Prerequisites

- Python 3.12+
- Docker (for testing)
- Home Assistant development environment (optional)

### Local Development

1. Clone the repository:
   ```bash
   git clone https://github.com/larrifax/ha-google-home.git
   cd ha-google-home
   ```

2. Set up Python environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r google_home/requirements.txt
   ```

3. Install development dependencies:
   ```bash
   pip install black ruff mypy pytest
   ```

### Code Style

- Follow PEP 8 guidelines
- Use type hints for all functions
- Keep functions focused and small
- Write descriptive variable names
- Add docstrings to classes and functions

### Testing

```bash
# Run syntax check
python3 -m py_compile google_home/rootfs/app/*.py

# Run type checking (if mypy is installed)
mypy google_home/rootfs/app/

# Format code (if black is installed)
black google_home/rootfs/app/

# Lint code (if ruff is installed)
ruff check google_home/rootfs/app/
```

### Building Docker Image

```bash
cd google_home
docker build -t google-home-api:test .
```

### Testing the Add-on

1. Copy the add-on to your Home Assistant addons directory
2. Restart Home Assistant
3. Install and configure the add-on
4. Check logs for any issues

## Documentation

- Update DOCS.md for user-facing changes
- Update CHANGELOG.md following Keep a Changelog format
- Update README.md if needed
- Add inline comments for complex logic

## Security

- Never commit credentials or tokens
- Update dependencies regularly
- Fix security vulnerabilities promptly
- Use the gh-advisory-database to check dependencies

## Review Process

1. All PRs require review before merging
2. CI checks must pass
3. Code must follow style guidelines
4. Documentation must be updated
5. Security scan must pass

## Questions?

Open an issue or discussion if you have questions!

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
