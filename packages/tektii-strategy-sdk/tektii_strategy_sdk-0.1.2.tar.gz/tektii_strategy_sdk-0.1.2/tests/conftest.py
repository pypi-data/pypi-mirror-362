"""Shared pytest fixtures and configuration."""

from datetime import datetime
from typing import Any, Dict

import pytest

from tektii_sdk import StrategyConfig
from tektii_sdk.strategy import MarketData, TimeFrame


@pytest.fixture  # type: ignore[misc]
def mock_config() -> StrategyConfig:
    """Create a mock strategy configuration."""
    return StrategyConfig(
        name="TestStrategy",
        version="1.0.0",
        symbols=["TEST1", "TEST2"],
        timeframes=[TimeFrame.M5],
        initial_capital=10000.0,
        max_positions=2,
        risk_per_trade=0.02,
        parameters={"param1": 100, "param2": "test"},
    )


@pytest.fixture  # type: ignore[misc]
def sample_market_data() -> MarketData:
    """Create sample market data."""
    return MarketData(
        symbol="TEST1",
        timestamp=datetime.now(),
        bid=100.0,
        ask=100.1,
        last=100.05,
        volume=1000000,
        open=99.0,
        high=101.0,
        low=98.5,
        close=100.05,
    )


@pytest.fixture  # type: ignore[misc]
def instrument_mapping() -> Dict[int, str]:
    """Create a sample instrument mapping."""
    return {1: "BTC-USD", 2: "ETH-USD", 3: "TEST1", 4: "TEST2"}


# Configure pytest
def pytest_configure(config: Any) -> None:
    """Configure pytest with custom markers."""
    config.addinivalue_line("markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')")
    config.addinivalue_line("markers", "integration: marks tests as integration tests")
    config.addinivalue_line("markers", "unit: marks tests as unit tests")
