"""Simulated Interactive Brokers API implementation."""

from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Optional

from tektii_sdk.apis.base import SimulatedAPI
from tektii_sdk.collector import ActionCollector
from tektii_sdk.strategy import MarketData, Order, Position


@dataclass
class Contract:
    """IB-style contract definition."""

    symbol: str
    # Security type: STK (stock), OPT (option), FUT (future), etc.
    # STK, OPT, FUT, CASH, BOND, CFD, FOP, WAR, IOPT, FWD, BAG, IND,
    # BILL, FUND, FIXED, SLB, NEWS, CMDTY, BSK, ICU, ICS
    secType: str = "STK"
    exchange: str = "SMART"
    currency: str = "USD"
    primaryExchange: Optional[str] = None

    def __str__(self) -> str:
        """Return a string representation of the contract."""
        return f"{self.symbol}-{self.secType}-{self.exchange}-{self.currency}"


@dataclass
class IBOrder:
    """IB-style order definition."""

    action: str  # BUY, SELL
    totalQuantity: float
    orderType: str  # MKT, LMT, STP, STP_LMT, TRAIL, TRAIL_LIMIT
    lmtPrice: Optional[float] = None
    auxPrice: Optional[float] = None  # Stop price for stop orders
    tif: str = "DAY"  # Time in force: DAY, GTC, IOC, GTD, OPG, FOK, DTC

    @classmethod
    def marketOrder(cls, action: str, quantity: float) -> "IBOrder":
        """Create a market order."""
        return cls(action=action, totalQuantity=quantity, orderType="MKT")

    @classmethod
    def limitOrder(cls, action: str, quantity: float, lmtPrice: float) -> "IBOrder":
        """Create a limit order."""
        return cls(action=action, totalQuantity=quantity, orderType="LMT", lmtPrice=lmtPrice)

    @classmethod
    def stopOrder(cls, action: str, quantity: float, stopPrice: float) -> "IBOrder":
        """Create a stop order."""
        return cls(action=action, totalQuantity=quantity, orderType="STP", auxPrice=stopPrice)


class SimulatedIB(SimulatedAPI):
    """Simulated Interactive Brokers API.

    Mimics the ib_insync API interface for seamless transition between backtesting and live trading.
    """

    def __init__(self, action_collector: ActionCollector):
        """Initialize the simulated IB API."""
        super().__init__(action_collector)
        self._positions: Dict[str, Position] = {}
        self._account_values: Dict[str, float] = {
            "NetLiquidation": 100000.0,
            "TotalCashValue": 100000.0,
            "GrossPositionValue": 0.0,
            "UnrealizedPnL": 0.0,
            "RealizedPnL": 0.0,
            "AvailableFunds": 100000.0,
            "ExcessLiquidity": 100000.0,
            "BuyingPower": 400000.0,  # 4:1 leverage
        }
        self._next_order_id = 1
        self._req_id_counter = 1
        self._market_data_subscriptions: Dict[int, Contract] = {}

    def connect(self, **kwargs: Any) -> None:
        """Connect to IB Gateway/TWS.

        Args:
            **kwargs: Connection parameters including:
                host: Host address (default: "127.0.0.1")
                port: Port number (default: 7497)
                clientId: Client ID (default: 1)
        """
        host = kwargs.get("host", "127.0.0.1")
        port = kwargs.get("port", 7497)
        clientId = kwargs.get("clientId", 1)

        self.logger.info(f"Simulated connection to IB at {host}:{port} with clientId={clientId}")
        self._connected = True

        # Emit initial account update
        self.emit_account_update(self._account_values.copy())

    def disconnect(self) -> None:
        """Disconnect from IB."""
        self.logger.info("Disconnecting from simulated IB")
        self._connected = False
        self._market_data_subscriptions.clear()

    def subscribe_market_data(self, symbols: List[str], **kwargs: Any) -> None:
        """Subscribe to market data for given symbols.

        Args:
            symbols: List of symbols to subscribe to
            **kwargs: Additional parameters (ignored)
        """
        for symbol in symbols:
            contract = Contract(symbol=symbol)
            req_id = self._get_next_req_id()
            self._market_data_subscriptions[req_id] = contract
            self._subscribed_symbols.add(symbol)
            self.logger.info(f"Subscribed to market data for {symbol} (reqId={req_id})")

    def reqMktData(
        self,
        contract: Contract,
        genericTickList: str = "",
        snapshot: bool = False,
        regulatorySnapshot: bool = False,
    ) -> int:
        """Request market data (IB-style method).

        Args:
            contract: Contract to get data for
            genericTickList: Generic tick list (ignored)
            snapshot: Whether to get snapshot (ignored)
            regulatorySnapshot: Whether to get regulatory snapshot (ignored)

        Returns:
            Request ID
        """
        req_id = self._get_next_req_id()
        self._market_data_subscriptions[req_id] = contract
        self._subscribed_symbols.add(contract.symbol)
        self.logger.info(f"Requested market data for {contract} (reqId={req_id})")
        return req_id

    def cancelMktData(self, reqId: int) -> None:
        """Cancel market data subscription.

        Args:
            reqId: Request ID to cancel
        """
        if reqId in self._market_data_subscriptions:
            contract = self._market_data_subscriptions.pop(reqId)
            self._subscribed_symbols.discard(contract.symbol)
            self.logger.info(f"Cancelled market data for reqId={reqId}")

    def place_order(self, order: Order) -> str:
        """Place an order (generic method).

        Args:
            order: Order to place

        Returns:
            Order ID
        """
        # Convert to IB-style order
        ib_order = self._convert_to_ib_order(order)
        contract = Contract(symbol=order.symbol)

        # Get next order ID
        order_id = self._get_next_order_id()

        # Use action collector to record the order
        self.action_collector.add_order(
            symbol=order.symbol,
            side=order.side,
            quantity=order.quantity,
            order_type=order.order_type,
            price=order.price,
            additional_params={"ib_order_id": str(order_id)},
        )

        self.logger.info(f"Placed order {order_id}: {ib_order} for {contract}")

        # Simulate immediate order acknowledgment
        self.emit_order_update(str(order_id), "submitted")

        return str(order_id)

    def placeOrder(self, contract: Contract, order: IBOrder) -> int:
        """Place an order (IB-style method).

        Args:
            contract: Contract to trade
            order: IB-style order

        Returns:
            Order ID
        """
        order_id = self._get_next_order_id()

        # Convert IB order to our internal format for action collector
        side = "buy" if order.action.upper() == "BUY" else "sell"
        order_type = self._convert_ib_order_type(order.orderType)

        self.action_collector.add_order(
            symbol=contract.symbol,
            side=side,
            quantity=order.totalQuantity,
            order_type=order_type,
            price=order.lmtPrice if order.orderType in ["LMT", "STP_LMT"] else order.auxPrice,
            additional_params={
                "ib_order_id": str(order_id),
                "tif": order.tif,
                "contract": str(contract),
            },
        )

        self.logger.info(f"Placed IB order {order_id}: {order} for {contract}")

        # Simulate immediate order acknowledgment
        self.emit_order_update(str(order_id), "submitted")

        return order_id

    def cancel_order(self, order_id: str) -> None:
        """Cancel an order.

        Args:
            order_id: Order ID to cancel
        """
        self.action_collector.add_cancel_order(order_id)
        self.logger.info(f"Cancelled order {order_id}")

        # Simulate immediate cancellation acknowledgment
        self.emit_order_update(order_id, "cancelled")

    def cancelOrder(self, orderId: int) -> None:
        """Cancel an order (IB-style method).

        Args:
            orderId: Order ID to cancel
        """
        self.cancel_order(str(orderId))

    def get_positions(self) -> Dict[str, Position]:
        """Get all open positions.

        Returns:
            Dictionary of symbol to position
        """
        return self._positions.copy()

    def positions(self) -> List[Dict[str, Any]]:
        """Return current portfolio positions with P&L calculations.

        Returns:
            List of position dictionaries
        """
        current_positions = []
        for symbol, pos in self._positions.items():
            current_positions.append(
                {
                    "contract": Contract(symbol=symbol),
                    "position": pos.quantity,
                    "avgCost": pos.average_price,
                    "marketPrice": pos.current_price,
                    "unrealizedPNL": pos.unrealized_pnl,
                    "realizedPNL": 0.0,  # Not tracked in simple implementation
                }
            )
        return current_positions

    def get_account_info(self) -> Dict[str, Any]:
        """Get account information.

        Returns:
            Dictionary of account values
        """
        return self._account_values.copy()

    def accountValues(self) -> List[Dict[str, Any]]:
        """Get account values (IB-style method).

        Returns:
            List of account value dictionaries
        """
        values = []
        for key, value in self._account_values.items():
            values.append(
                {
                    "account": "DU123456",  # Simulated account
                    "tag": key,
                    "value": str(value),
                    "currency": "USD",
                }
            )
        return values

    def _convert_to_ib_order(self, order: Order) -> IBOrder:
        """Convert generic order to IB order.

        Args:
            order: Generic order

        Returns:
            IB-style order
        """
        action = "BUY" if order.side == "buy" else "SELL"

        if order.order_type == "market":
            return IBOrder.marketOrder(action, order.quantity)
        elif order.order_type == "limit":
            if order.price is None:
                raise ValueError("Limit order requires a price")
            return IBOrder.limitOrder(action, order.quantity, order.price)
        elif order.order_type == "stop":
            if order.price is None:
                raise ValueError("Stop order requires a price")
            return IBOrder.stopOrder(action, order.quantity, order.price)
        else:
            # Default to market order
            return IBOrder.marketOrder(action, order.quantity)

    def _convert_ib_order_type(self, ib_type: str) -> str:
        """Convert IB order type to generic type.

        Args:
            ib_type: IB order type

        Returns:
            Generic order type
        """
        mapping = {
            "MKT": "market",
            "LMT": "limit",
            "STP": "stop",
            "STP_LMT": "stop_limit",
        }
        return mapping.get(ib_type, "market")

    def _get_next_order_id(self) -> int:
        """Get next order ID.

        Returns:
            Next order ID
        """
        order_id = self._next_order_id
        self._next_order_id += 1
        return order_id

    def _get_next_req_id(self) -> int:
        """Get next request ID.

        Returns:
            Next request ID
        """
        req_id = self._req_id_counter
        self._req_id_counter += 1
        return req_id

    # Convenience methods for IB-style callbacks
    def pendingTickersEvent(self, callback: Callable) -> None:
        """Register callback for market data updates.

        Args:
            callback: Callback function
        """

        def wrapper(data: MarketData) -> None:
            # Convert to IB-style ticker format
            ticker = {
                "contract": Contract(symbol=data.symbol),
                "bid": data.bid,
                "ask": data.ask,
                "last": data.last,
                "volume": data.volume,
                "time": data.timestamp,
            }
            callback([ticker])

        self.register_callback("market_data", wrapper)

    def orderStatusEvent(self, callback: Callable) -> None:
        """Register callback for order status updates.

        Args:
            callback: Callback function
        """
        self.register_callback("order_update", callback)

    def positionEvent(self, callback: Callable) -> None:
        """Register callback for position updates.

        Args:
            callback: Callback function
        """
        self.register_callback("position_update", callback)

    def accountValueEvent(self, callback: Callable) -> None:
        """Register callback for account updates.

        Args:
            callback: Callback function
        """
        self.register_callback("account_update", callback)
