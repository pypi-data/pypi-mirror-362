"""Exception classes for the backtest SDK."""


class BacktestSDKError(Exception):
    """Base exception for all SDK errors."""


class StrategyError(BacktestSDKError):
    """Error related to strategy execution."""


class ValidationError(BacktestSDKError):
    """Error related to validation."""


class ConfigurationError(BacktestSDKError):
    """Error related to configuration."""


class ConnectionError(BacktestSDKError):
    """Error related to API connections."""


class OrderError(BacktestSDKError):
    """Error related to order placement or management."""


class DataError(BacktestSDKError):
    """Error related to market data."""
