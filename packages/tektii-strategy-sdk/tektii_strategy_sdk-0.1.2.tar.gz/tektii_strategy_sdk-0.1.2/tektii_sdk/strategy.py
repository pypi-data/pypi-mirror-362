"""Base strategy class and configuration for backtest strategies."""

import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Tuple

from pydantic import BaseModel, Field

from tektii_sdk.collector import ActionCollector
from tektii_sdk.exceptions import StrategyError

logger = logging.getLogger(__name__)


class TimeFrame(str, Enum):
    """Supported timeframes for market data."""

    TICK = "tick"
    S1 = "1s"
    S5 = "5s"
    S15 = "15s"
    S30 = "30s"
    M1 = "1m"
    M5 = "5m"
    M15 = "15m"
    M30 = "30m"
    H1 = "1h"
    H4 = "4h"
    D1 = "1d"
    W1 = "1w"
    MN1 = "1M"


class StrategyConfig(BaseModel):
    """Configuration for a strategy instance."""

    name: str = Field(..., description="Strategy name")
    version: str = Field("1.0.0", description="Strategy version")
    symbols: List[str] = Field(default_factory=list, description="Symbols to trade")
    timeframes: List[TimeFrame] = Field(default_factory=lambda: [TimeFrame.M5], description="Timeframes to subscribe to")
    initial_capital: float = Field(10000.0, description="Initial capital")
    max_positions: int = Field(5, description="Maximum concurrent positions")
    risk_per_trade: float = Field(0.02, description="Risk per trade as fraction of capital")
    parameters: Dict[str, Any] = Field(default_factory=dict, description="Strategy-specific parameters")

    class Config:
        """Pydantic configuration."""

        use_enum_values = True


@dataclass
class MarketData:
    """Market data event."""

    symbol: str
    timestamp: datetime
    bid: float
    ask: float
    last: float
    volume: int
    timeframe: Optional[TimeFrame] = None
    open: Optional[float] = None
    high: Optional[float] = None
    low: Optional[float] = None
    close: Optional[float] = None

    @property
    def mid(self) -> float:
        """Calculate mid price."""
        return (self.bid + self.ask) / 2

    @property
    def spread(self) -> float:
        """Calculate spread."""
        return self.ask - self.bid


@dataclass
class Order:
    """Order representation."""

    symbol: str
    side: str  # "buy" or "sell"
    quantity: float
    order_type: str = "market"  # "market", "limit", "stop", "stop_limit"
    price: Optional[float] = None  # Limit price for limit orders, stop price for stop orders
    order_id: Optional[str] = None

    def __post_init__(self) -> None:
        """Validate order parameters."""
        # Validate side
        if self.side not in ["buy", "sell"]:
            raise ValueError(f"Invalid order side: {self.side}")

        # Validate quantity
        if self.quantity <= 0:
            raise ValueError(f"Order quantity must be positive: {self.quantity}")

        # Validate order type and price requirements
        if self.order_type in ["limit", "stop", "stop_limit"] and self.price is None:
            raise ValueError(f"Price required for {self.order_type} orders")

        # Validate order type
        valid_types = ["market", "limit", "stop", "stop_limit"]
        if self.order_type not in valid_types:
            raise ValueError(f"Invalid order type: {self.order_type}. Must be one of {valid_types}")


@dataclass
class Position:
    """Position representation."""

    symbol: str
    quantity: float
    average_price: float
    current_price: float
    unrealized_pnl: float = field(init=False)

    def __post_init__(self) -> None:
        """Calculate initial PnL."""
        self.update_pnl(self.current_price)

    def update_pnl(self, current_price: float) -> None:
        """Update position PnL."""
        self.current_price = current_price
        self.unrealized_pnl = (current_price - self.average_price) * self.quantity


class Strategy(ABC):
    """Base class for all trading strategies."""

    def __init__(self, config: StrategyConfig):
        """Initialize strategy with configuration."""
        self.config = config
        self.action_collector = ActionCollector()
        self._positions: Dict[str, Position] = {}
        self._pending_orders: Dict[str, Order] = {}
        self._market_data_callbacks: List[Callable] = []
        self._order_update_callbacks: List[Callable] = []
        self._position_update_callbacks: List[Callable] = []
        self._initialized = False
        self.events_received: List[Tuple[str, Any]] = []

        # Setup logging
        self.logger = logging.getLogger(f"{__name__}.{self.config.name}")

    @abstractmethod
    def on_start(self) -> None:
        """Execute setup operations when the strategy is initialized.

        Override this method to perform any setup operations.
        """

    @abstractmethod
    def on_market_data(self, data: MarketData) -> None:
        """Process incoming market data.

        This method should be overridden to implement strategy logic based on market data.

        Args:
            data: Market data event
        """

    def on_order_update(self, order_id: str, status: str, filled_quantity: float = 0) -> None:
        """Process order updates.

        This method is called when an order status changes (e.g., filled, cancelled). It can be overridden to implement
        custom order handling logic.

        Args:
            order_id: Order identifier
            status: New order status
            filled_quantity: Quantity filled (if applicable)
        """
        self.logger.info(f"Order {order_id} updated: {status}, filled: {filled_quantity}")

    def on_position_update(self, position: Position) -> None:
        """Process position updates.

        This method is called when a position is updated (e.g., new position, PnL change). It can be overridden to
        implement custom position handling logic.

        Args:
            position: Updated position
        """
        self._positions[position.symbol] = position
        self.logger.info(f"Position updated: {position.symbol}, PnL: {position.unrealized_pnl}")

    def on_stop(self) -> None:
        """Execute cleanup operations when the strategy is stopped.

        This method is called when the strategy is shutting down.

        Override this method to perform cleanup operations.
        """
        self.logger.info("Strategy stopped")

    def buy(
        self,
        symbol: str,
        quantity: float,
        order_type: str = "market",
        price: Optional[float] = None,
    ) -> str:
        """Place a buy order.

        Args:
            symbol: Symbol to buy
            quantity: Quantity to buy
            order_type: Order type (market, limit, stop, stop_limit)
            price: Price for limit/stop orders

        Returns:
            Order ID

        Raises:
            StrategyError: If order validation fails
        """
        order = Order(symbol=symbol, side="buy", quantity=quantity, order_type=order_type, price=price)
        return self._place_order(order)

    def sell(
        self,
        symbol: str,
        quantity: float,
        order_type: str = "market",
        price: Optional[float] = None,
    ) -> str:
        """Place a sell order.

        Args:
            symbol: Symbol to sell
            quantity: Quantity to sell
            order_type: Order type (market, limit, stop, stop_limit)
            price: Price for limit/stop orders

        Returns:
            Order ID

        Raises:
            StrategyError: If order validation fails
        """
        order = Order(symbol=symbol, side="sell", quantity=quantity, order_type=order_type, price=price)
        return self._place_order(order)

    def cancel_order(self, order_id: str) -> None:
        """Cancel an order.

        Args:
            order_id: Order ID to cancel
        """
        if order_id in self._pending_orders:
            self.action_collector.add_cancel_order(order_id)
            del self._pending_orders[order_id]
            self.logger.info(f"Order {order_id} cancelled")
        else:
            self.logger.warning(f"Order {order_id} not found")

    def get_position(self, symbol: str) -> Optional[Position]:
        """Get position for a symbol.

        Args:
            symbol: Symbol to get position for

        Returns:
            Position or None if no position exists
        """
        return self._positions.get(symbol)

    def get_all_positions(self) -> Dict[str, Position]:
        """Get all open positions.

        Returns:
            Dictionary of symbol to position
        """
        return self._positions.copy()

    def log(self, message: str, level: str = "info") -> None:
        """Log a message.

        Args:
            message: Message to log
            level: Log level (debug, info, warning, error)
        """
        self.action_collector.add_log(message, level)
        getattr(self.logger, level, self.logger.info)(message)

    def _place_order(self, order: Order) -> str:
        """Place an order after validation.

        This method handles order validation and placement. It should not be overridden by subclasses.

        Args:
            order: Order to place

        Returns:
            Order ID
        """
        # Validate order against risk limits
        if not self._validate_order(order):
            raise StrategyError(f"Order validation failed for {order}")

        # Generate order ID
        order_id = self.action_collector.add_order(
            symbol=order.symbol,
            side=order.side,
            quantity=order.quantity,
            order_type=order.order_type,
            price=order.price,
        )

        order.order_id = order_id
        self._pending_orders[order_id] = order

        self.logger.info(f"Order placed: {order}")
        return order_id

    def _validate_order(self, order: Order) -> bool:
        """Validate order against risk limits.

        Args:
            order: Order to validate

        Returns:
            True if order is valid
        """
        # Check max positions
        if len(self._positions) >= self.config.max_positions and order.symbol not in self._positions:
            self.logger.warning("Max positions reached")
            return False

        # Additional validation can be added here
        return True

    def register_market_data_callback(self, callback: Callable) -> None:
        """Register a callback for market data events.

        Args:
            callback: Callback function
        """
        self._market_data_callbacks.append(callback)

    def emit_market_data(self, data: MarketData) -> None:
        """Emit market data to all registered callbacks.

        Args:
            data: Market data to emit
        """
        if not self._initialized:
            self.logger.warning("Strategy not initialized, ignoring market data")
            return

        try:
            # Call strategy's on_market_data first
            self.on_market_data(data)
        except Exception as e:
            self.logger.error(f"Error in on_market_data: {e}", exc_info=True)
            self.action_collector.add_log(f"Error in strategy: {str(e)}", "error")

        # Then call any registered callbacks
        for callback in self._market_data_callbacks:
            try:
                callback(data)
            except Exception as e:
                self.logger.error(f"Error in market data callback: {e}", exc_info=True)

    def initialize(self) -> None:
        """Initialize the strategy."""
        if self._initialized:
            return

        self.logger.info(f"Initializing strategy: {self.config.name}")
        self.on_start()
        self._initialized = True

    def shutdown(self) -> None:
        """Shutdown the strategy."""
        if not self._initialized:
            return

        self.logger.info(f"Shutting down strategy: {self.config.name}")
        self.on_stop()
        self._initialized = False
