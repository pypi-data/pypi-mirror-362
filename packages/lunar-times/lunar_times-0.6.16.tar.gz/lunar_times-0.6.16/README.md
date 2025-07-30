# Lunar Times

[![CI](https://github.com/cscortes/lunar-times/workflows/CI/badge.svg)](https://github.com/cscortes/lunar-times/actions)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![PyPI version](https://badge.fury.io/py/lunar-times.svg)](https://badge.fury.io/py/lunar-times)
[![Coverage](https://codecov.io/gh/cscortes/lunar-times/branch/main/graph/badge.svg)](https://codecov.io/gh/cscortes/lunar-times)

A command-line Python application that calculates moonrise and moonset times for any location. The application integrates with external APIs to provide accurate astronomical data with proper timezone handling.

## Features

- 🌙 Calculate moonrise and moonset times for any US city and state
- 📍 Automatic coordinate resolution using OpenStreetMap geocoding
- 🕐 Timezone-aware calculations with proper daylight saving time handling
- 🔧 Debug mode for development and testing
- 🚀 Clean command-line interface with clear output formatting
- ✅ **Enterprise-grade CI/CD** with automated testing across multiple Python versions and platforms

## Quick Start

```bash
# Install dependencies
make install

# Run the application
make run

# Or use debug mode (defaults to El Paso, TX)
make run-debug

# Run tests
make test

# Check code quality
make check
```

## Example Usage

```bash
$ lunar-times
Enter the city: Austin
Enter the state: TX
# Moon rise/set times in (Timezone: America/Chicago -6.0) on 2024-01-15:
-  RISE: 10:45 PM
-  SET: 11:30 AM
```

## Documentation

- **[Usage Guide](docs/USAGE.md)** - Detailed usage instructions and examples
- **[Testing Documentation](docs/TEST.md)** - Comprehensive testing documentation and coverage analysis
- **[Setup Guide](docs/SETUP.md)** - Installation and configuration instructions
- **[Invisible Character Detection](scripts/invisible_chars_commands.md)** - Tools for detecting and removing invisible characters in AI-generated code
- **[Architecture](docs/ARCH.md)** - Technical architecture and design documentation
- **[Changelog](docs/CHANGELOG.md)** - Version history and release notes
- **[Failure Analysis](docs/FAILURE.md)** - Troubleshooting and known issues

## Development & CI/CD

This project uses **GitHub Actions** for comprehensive automated testing and deployment. All workflows are **live and operational**:

### Continuous Integration ✅
- **Multi-Python Testing**: Automated testing on Python 3.8, 3.9, 3.10, 3.11, and 3.12
- **Cross-Platform**: Tests run on Ubuntu, Windows, and macOS 
- **Quality Gates**: Linting, type checking, test coverage, and security scanning
- **Fast Feedback**: Quick validation jobs provide rapid feedback on pull requests

### Automated Deployment ✅
- **PyPI Publishing**: Automatic package publishing on version tags
- **GitHub Releases**: Automated release creation with changelog integration  
- **Health Monitoring**: Weekly API health checks with automatic issue creation

### Operational Workflows
- **CI Pipeline** ([`.github/workflows/ci.yml`](.github/workflows/ci.yml)) - 212 lines of comprehensive testing automation
- **Release Pipeline** ([`.github/workflows/release.yml`](.github/workflows/release.yml)) - 104 lines of deployment automation
- **Health Monitoring** ([`.github/workflows/health-check.yml`](.github/workflows/health-check.yml)) - 57 lines of API monitoring

### Development Workflow
```bash
# All development commands work with CI
make test          # Runs same tests as CI
make check         # Runs all quality checks  
make build-package # Builds package like CI
```

View live [workflow runs](https://github.com/cscortes/lunar-times/actions) and [automation details](.github/workflows/).

## Requirements

- Python 3.8+
- [uv](https://docs.astral.sh/uv/) package manager
- Internet connection for API calls
- Dependencies: requests, geopy, timezonefinder, pytz

## License

This project is licensed under the terms in the [LICENSE](LICENSE) file.
