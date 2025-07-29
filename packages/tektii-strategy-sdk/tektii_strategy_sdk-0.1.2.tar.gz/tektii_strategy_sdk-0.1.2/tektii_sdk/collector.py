"""Action collector for capturing strategy actions during event processing."""

import threading
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional


class ActionType(str, Enum):
    """Types of actions that can be collected."""

    PLACE_ORDER = "place_order"
    CANCEL_ORDER = "cancel_order"
    MODIFY_ORDER = "modify_order"


class LogLevel(str, Enum):
    """Log levels."""

    DEBUG = "debug"
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"


@dataclass
class OrderAction:
    """Represents an order action."""

    action_type: ActionType
    symbol: str
    side: str  # "buy" or "sell"
    quantity: float
    order_type: str = "market"
    price: Optional[float] = None
    stop_price: Optional[float] = None
    order_id: Optional[str] = None
    additional_params: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.utcnow)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "action_type": self.action_type,
            "symbol": self.symbol,
            "side": self.side,
            "quantity": self.quantity,
            "order_type": self.order_type,
            "price": self.price,
            "stop_price": self.stop_price,
            "order_id": self.order_id,
            "additional_params": self.additional_params,
            "timestamp": self.timestamp.isoformat(),
        }


@dataclass
class LogEntry:
    """Represents a log entry."""

    level: LogLevel
    message: str
    timestamp: datetime = field(default_factory=datetime.utcnow)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "level": self.level,
            "message": self.message,
            "timestamp": self.timestamp.isoformat(),
        }


class ActionCollector:
    """Thread-safe collector for strategy actions.

    This class collects all actions (orders, logs, etc.) that occur during event processing and makes them available for the gRPC response.
    """

    def __init__(self) -> None:
        """Initialize the action collector."""
        self._orders: List[OrderAction] = []
        self._logs: List[LogEntry] = []
        self._metadata: Dict[str, str] = {}
        self._lock = threading.Lock()
        self._order_counter = 0

    def clear(self) -> None:
        """Clear all collected actions.

        Should be called at the start of each event processing cycle.
        """
        with self._lock:
            self._orders.clear()
            self._logs.clear()
            self._metadata.clear()

    def add_order(
        self,
        symbol: str,
        side: str,
        quantity: float,
        order_type: str = "market",
        price: Optional[float] = None,
        additional_params: Optional[Dict[str, Any]] = None,
    ) -> str:
        """Add a place order action.

        Args:
            symbol: Trading symbol
            side: Order side ("buy" or "sell")
            quantity: Order quantity
            order_type: Order type
            price: Order price (limit price for limit orders, stop price for stop orders)
            additional_params: Additional order parameters

        Returns:
            Generated order ID
        """
        with self._lock:
            order_id = self._generate_order_id()

            # For stop orders, store the price as stop_price in the action
            stop_price = None
            if order_type in ["stop", "stop_limit"]:
                stop_price = price
                # For stop_limit, price would be the limit price (if different from stop)
                # but for simplicity, we use the same price for both

            action = OrderAction(
                action_type=ActionType.PLACE_ORDER,
                symbol=symbol,
                side=side,
                quantity=quantity,
                order_type=order_type,
                price=price if order_type in ["limit", "stop_limit"] else None,
                stop_price=stop_price,
                order_id=order_id,
                additional_params=additional_params or {},
            )
            self._orders.append(action)
            return order_id

    def add_cancel_order(self, order_id: str) -> None:
        """Add a cancel order action.

        Args:
            order_id: ID of order to cancel
        """
        with self._lock:
            action = OrderAction(
                action_type=ActionType.CANCEL_ORDER,
                symbol="",  # Not needed for cancellation
                side="",
                quantity=0,
                order_id=order_id,
            )
            self._orders.append(action)

    def add_modify_order(self, order_id: str, quantity: Optional[float] = None, price: Optional[float] = None) -> None:
        """Add a modify order action.

        Args:
            order_id: ID of order to modify
            quantity: New quantity (if changing)
            price: New price (if changing)
        """
        if not order_id:
            raise ValueError("Order ID is required for modify order action")

        with self._lock:
            params = {}
            if quantity is not None:
                if quantity <= 0:
                    raise ValueError(f"Order quantity must be positive: {quantity}")
                params["new_quantity"] = quantity
            if price is not None:
                if price <= 0:
                    raise ValueError(f"Order price must be positive: {price}")
                params["new_price"] = price

            if not params:
                raise ValueError("At least one parameter must be specified for modify order")

            action = OrderAction(
                action_type=ActionType.MODIFY_ORDER,
                symbol="",  # Not needed for modification
                side="",
                quantity=0,
                order_id=order_id,
                additional_params=params,
            )
            self._orders.append(action)

    def add_log(self, message: str, level: str = "info") -> None:
        """Add a log entry.

        Args:
            message: Log message
            level: Log level
        """
        with self._lock:
            log_level = LogLevel(level.lower())
            entry = LogEntry(level=log_level, message=message)
            self._logs.append(entry)

    def add_metadata(self, key: str, value: str) -> None:
        """Add metadata.

        Args:
            key: Metadata key
            value: Metadata value
        """
        with self._lock:
            self._metadata[key] = value

    def get_actions(self) -> Dict[str, Any]:
        """Get all collected actions.

        Returns:
            Dictionary containing orders, logs, and metadata
        """
        with self._lock:
            return {
                "orders": [order.to_dict() for order in self._orders],
                "logs": [log.to_dict() for log in self._logs],
                "metadata": self._metadata.copy(),
            }

    def get_orders(self) -> List[OrderAction]:
        """Get collected order actions.

        Returns:
            List of order actions
        """
        with self._lock:
            return self._orders.copy()

    def get_logs(self) -> List[LogEntry]:
        """Get collected log entries.

        Returns:
            List of log entries
        """
        with self._lock:
            return self._logs.copy()

    def get_metadata(self) -> Dict[str, str]:
        """Get collected metadata.

        Returns:
            Dictionary of metadata
        """
        with self._lock:
            return self._metadata.copy()

    def _generate_order_id(self) -> str:
        """Generate a unique order ID.

        Returns:
            Unique order ID
        """
        self._order_counter += 1
        timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
        return f"ORD-{timestamp}-{self._order_counter:06d}-{uuid.uuid4().hex[:8]}"

    def __repr__(self) -> str:
        """Return a string representation of the collector."""
        with self._lock:
            return f"ActionCollector(orders={len(self._orders)}, " f"logs={len(self._logs)}, metadata_keys={list(self._metadata.keys())})"
