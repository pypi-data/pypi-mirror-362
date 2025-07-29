# Contributing to Tektii Strategy SDK

Thank you for your interest in contributing to the Tektii Strategy SDK! This document provides guidelines and instructions for contributing.

## Code of Conduct

By participating in this project, you agree to abide by our Code of Conduct:
- Be respectful and inclusive
- Welcome newcomers and help them get started
- Focus on what is best for the community
- Show empathy towards other community members

## How to Contribute

### Reporting Issues

Before creating an issue, please check if it already exists. When creating a new issue:

1. Use a clear and descriptive title
2. Provide a detailed description of the problem
3. Include steps to reproduce the issue
4. Mention your environment (OS, Python version, SDK version)
5. Include relevant error messages or logs

### Suggesting Features

Feature requests are welcome! Please:

1. Check if the feature has already been requested
2. Provide a clear use case
3. Explain how it would benefit users
4. Consider if it aligns with the project's goals

### Pull Requests

1. **Fork the repository** and create your branch from `main`
2. **Set up your development environment**:
   ```bash
   git clone https://github.com/tektii/tektii-strategy-sdk.git
   cd tektii-strategy-sdk
   pip install -e ".[dev]"
   pre-commit install
   ```

3. **Make your changes**:
   - Write clear, concise commit messages
   - Follow the coding style (see below)
   - Add tests for new functionality
   - Update documentation as needed

4. **Test your changes**:
   ```bash
   # Run tests
   pytest tests/

   # Run linting
   make lint

   # Format code
   make format
   ```

5. **Submit your PR**:
   - Provide a clear description of the changes
   - Reference any related issues
   - Ensure all tests pass
   - Request review from maintainers

## Development Setup

### Prerequisites

- Python 3.8 or higher
- pip and virtualenv
- protoc (Protocol Buffers compiler)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/tektii/tektii-strategy-sdk.git
   cd tektii-strategy-sdk
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install in development mode:
   ```bash
   pip install -e ".[dev,examples]"
   ```

4. Install pre-commit hooks:
   ```bash
   pre-commit install
   ```

5. Generate protobuf files:
   ```bash
   make proto
   ```

## Coding Standards

### Python Style Guide

We follow PEP 8 with some modifications:
- Line length: 150 characters
- Use type hints for all functions
- Docstrings: Google style

Example:
```python
def calculate_position_size(
    capital: float,
    risk_percent: float,
    stop_loss: float
) -> float:
    """Calculate position size based on risk management rules.

    Args:
        capital: Total available capital
        risk_percent: Risk percentage per trade (0-1)
        stop_loss: Stop loss distance in price units

    Returns:
        Position size in units

    Raises:
        ValueError: If parameters are invalid
    """
    if risk_percent <= 0 or risk_percent > 1:
        raise ValueError("Risk percent must be between 0 and 1")

    return (capital * risk_percent) / stop_loss
```

### Testing Guidelines

- Write tests for all new functionality
- Aim for at least 80% code coverage
- Use pytest fixtures for setup
- Mock external dependencies
- Test both success and failure cases

Example:
```python
import pytest
from unittest.mock import Mock

def test_strategy_initialization(mock_config):
    """Test strategy initializes correctly."""
    strategy = MyStrategy(mock_config)
    strategy.initialize()

    assert strategy._initialized
    assert strategy.on_start_called
```

### Documentation

- All public APIs must have docstrings
- Update README.md for user-facing changes
- Add examples for new features
- Keep documentation in sync with code

## Project Structure

```
tektii-strategy-sdk/
├── tektii_sdk/        # Main package
│   ├── __init__.py
│   ├── strategy.py      # Base strategy class
│   ├── server.py        # gRPC server
│   ├── apis/            # Simulated trading APIs
│   └── proto/           # Generated protobuf files
├── examples/            # Example strategies
├── tests/               # Test suite
├── docs/                # Documentation
└── proto/               # Protocol buffer definitions
```

## Release Process

1. Update version in `tektii_sdk/__version__.py`
2. Update CHANGELOG.md
3. Create a release PR
4. After merge, tag the release
5. Build and publish to PyPI

## Getting Help

- Check the documentation
- Look through existing issues
- Ask in discussions
- Contact maintainers

## Recognition

Contributors will be recognized in:
- The project's README
- Release notes
- GitHub contributors page

Thank you for contributing to make this project better!
