"""Base class for simulated trading APIs."""

import logging
from abc import ABC, abstractmethod
from typing import Any, Callable, Dict, List

from tektii_sdk.collector import ActionCollector
from tektii_sdk.strategy import MarketData, Order, Position


class SimulatedAPI(ABC):
    """Base class for all simulated trading platform APIs."""

    def __init__(self, action_collector: ActionCollector) -> None:
        """Initialize the simulated API.

        Args:
            action_collector: Action collector for capturing trading actions
        """
        self.action_collector = action_collector
        self.logger = logging.getLogger(self.__class__.__name__)
        self._callbacks: Dict[str, List[Callable]] = {
            "market_data": [],
            "order_update": [],
            "position_update": [],
            "account_update": [],
            "error": [],
        }
        self._connected = False
        self._subscribed_symbols: set = set()

    @abstractmethod
    def connect(self, **kwargs: Any) -> None:
        """Connect to the simulated trading platform.

        Args:
            **kwargs: Connection parameters
        """

    @abstractmethod
    def disconnect(self) -> None:
        """Disconnect from the simulated trading platform."""

    @abstractmethod
    def subscribe_market_data(self, symbols: List[str], **kwargs: Any) -> None:
        """Subscribe to market data for given symbols.

        Args:
            symbols: List of symbols to subscribe to
            **kwargs: Additional subscription parameters
        """

    @abstractmethod
    def place_order(self, order: Order) -> str:
        """Place an order.

        Args:
            order: Order to place

        Returns:
            Order ID
        """

    @abstractmethod
    def cancel_order(self, order_id: str) -> None:
        """Cancel an order.

        Args:
            order_id: ID of order to cancel
        """

    @abstractmethod
    def get_positions(self) -> Dict[str, Position]:
        """Get all open positions.

        Returns:
            Dictionary of symbol to position
        """

    @abstractmethod
    def get_account_info(self) -> Dict[str, Any]:
        """Get account information.

        Returns:
            Dictionary of account information
        """

    def register_callback(self, event_type: str, callback: Callable) -> None:
        """Register a callback for specific event types.

        Args:
            event_type: Type of event ("market_data", "order_update", etc.)
            callback: Callback function
        """
        if event_type not in self._callbacks:
            raise ValueError(f"Unknown event type: {event_type}")

        self._callbacks[event_type].append(callback)
        self.logger.debug(f"Registered callback for {event_type}")

    def emit_market_data(self, data: MarketData) -> None:
        """Emit market data to all registered callbacks.

        This method is called by the gRPC server when new market data arrives.
        It synchronously calls all registered callbacks.

        Args:
            data: Market data to emit
        """
        for callback in self._callbacks["market_data"]:
            try:
                callback(data)
            except Exception as e:
                self.logger.error(f"Error in market data callback: {e}")
                self._emit_error(f"Market data callback error: {e}")

    def emit_order_update(self, order_id: str, status: str, **kwargs: Any) -> None:
        """Emit order update to all registered callbacks.

        Args:
            order_id: Order ID
            status: Order status
            **kwargs: Additional order update data
        """
        for callback in self._callbacks["order_update"]:
            try:
                callback(order_id, status, **kwargs)
            except Exception as e:
                self.logger.error(f"Error in order update callback: {e}")
                self._emit_error(f"Order update callback error: {e}")

    def emit_position_update(self, position: Position) -> None:
        """Emit position update to all registered callbacks.

        Args:
            position: Updated position
        """
        for callback in self._callbacks["position_update"]:
            try:
                callback(position)
            except Exception as e:
                self.logger.error(f"Error in position update callback: {e}")
                self._emit_error(f"Position update callback error: {e}")

    def emit_account_update(self, account_info: Dict[str, Any]) -> None:
        """Emit account update to all registered callbacks.

        Args:
            account_info: Account information
        """
        for callback in self._callbacks["account_update"]:
            try:
                callback(account_info)
            except Exception as e:
                self.logger.error(f"Error in account update callback: {e}")
                self._emit_error(f"Account update callback error: {e}")

    def _emit_error(self, error_message: str) -> None:
        """Emit error to all registered error callbacks.

        Args:
            error_message: Error message
        """
        for callback in self._callbacks["error"]:
            try:
                callback(error_message)
            except Exception as e:
                self.logger.error(f"Error in error callback: {e}")

    @property
    def is_connected(self) -> bool:
        """Check if API is connected.

        Returns:
            True if connected
        """
        return self._connected

    def get_subscribed_symbols(self) -> List[str]:
        """Get list of subscribed symbols.

        Returns:
            List of subscribed symbols
        """
        return list(self._subscribed_symbols)
