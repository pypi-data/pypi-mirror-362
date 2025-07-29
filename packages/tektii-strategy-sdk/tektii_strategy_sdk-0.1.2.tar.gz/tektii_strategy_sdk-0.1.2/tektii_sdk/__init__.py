# tektii_sdk/__init__.py
"""Backtest Strategy SDK - Build and run trading strategies in containers."""

from tektii_sdk.__version__ import __version__
from tektii_sdk.apis import SimulatedIB, SimulatedMT4
from tektii_sdk.collector import ActionCollector
from tektii_sdk.exceptions import BacktestSDKError, StrategyError, ValidationError
from tektii_sdk.strategy import Strategy, StrategyConfig
from tektii_sdk.validator import ValidationResult, validate_module, validate_strategy

__all__ = [
    "__version__",
    "Strategy",
    "StrategyConfig",
    "SimulatedIB",
    "SimulatedMT4",
    "ActionCollector",
    "BacktestSDKError",
    "StrategyError",
    "ValidationError",
    "validate_strategy",
    "validate_module",
    "ValidationResult",
]
