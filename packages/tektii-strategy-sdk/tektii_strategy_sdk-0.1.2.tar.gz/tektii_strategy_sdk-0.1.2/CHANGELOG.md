# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Strategy validation system for pre-deployment checks
  - `tektii validate` CLI command
  - Python API: `validate_strategy()` and `validate_module()`
  - Comprehensive validation checks (structure, runtime, performance)
  - Detailed validation reports with errors, warnings, and info
- Example validation script (`examples/validate_strategy.py`)
- Validation documentation (`docs/validation.md`)
- Health check improvements in gRPC server

### Changed
- CLI now uses subcommands (`run` and `validate`)
  - Old syntax still supported for backwards compatibility
- Consolidated `stop_price` parameter into `price` parameter for orders
- Health check now starts with NOT_SERVING status until initialized
- Improved error messages and logging throughout

### Fixed
- grpcio-reflection warning by making it a required dependency
- Various test issues related to API changes

## [0.1.0] - Initial Release

### Added
- Initial release of the Tektii Strategy SDK
- Core `Strategy` base class for building trading strategies
- gRPC server implementation for event-driven backtesting
- Action collector for capturing trading decisions
- Simulated trading APIs:
  - Interactive Brokers (IB) API simulation
  - MetaTrader 4 (MT4) API simulation
- Example strategies:
  - Simple Moving Average crossover strategy
  - RSI mean reversion strategy
- Command-line interface (CLI) for running strategies
- Docker support with base images and compose configuration
- Comprehensive test suite
- Documentation and examples
- Pre-commit hooks for code quality
- GitHub Actions CI/CD workflow

### Changed
- N/A (initial release)

### Deprecated
- N/A (initial release)

### Removed
- N/A (initial release)

### Fixed
- N/A (initial release)

### Security
- Implemented secure container configuration
- Added input validation for all public APIs
- Restricted file system access in containers

## [0.1.0] - 2024-XX-XX (Planned)

### Added
- First public release on PyPI
- Complete documentation on Read the Docs
- Docker images published to Docker Hub

### Changed
- Stabilized public API

### Fixed
- All known issues from pre-release testing

---

## Version History Guide

### Major version (X.0.0)
- Breaking changes to the API
- Major architectural changes
- Removal of deprecated features

### Minor version (0.X.0)
- New features and functionality
- Non-breaking API additions
- New simulated trading platforms

### Patch version (0.0.X)
- Bug fixes
- Performance improvements
- Documentation updates
- Security patches

## Migration Guides

### Migrating from 0.x to 1.0
(To be added when 1.0 is released)

## Deprecation Policy

Features marked as deprecated will be maintained for at least two minor versions before removal. Deprecation warnings will be logged when deprecated features are used.

## Support Policy

- Latest version: Full support
- Previous minor version: Security updates only
- Older versions: Community support only

For questions about specific versions, please open an issue on GitHub.
