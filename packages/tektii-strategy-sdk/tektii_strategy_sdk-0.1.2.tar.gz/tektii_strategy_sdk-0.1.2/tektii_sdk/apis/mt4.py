"""Simulated MetaTrader 4 API implementation."""

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Any, Callable, Dict, List, Optional

from tektii_sdk.apis.base import SimulatedAPI
from tektii_sdk.collector import ActionCollector
from tektii_sdk.strategy import MarketData, Order, Position


class MT4OrderType(Enum):
    """MT4 order types."""

    OP_BUY = 0
    OP_SELL = 1
    OP_BUYLIMIT = 2
    OP_SELLLIMIT = 3
    OP_BUYSTOP = 4
    OP_SELLSTOP = 5


class MT4TimeFrame(Enum):
    """MT4 timeframes."""

    PERIOD_M1 = 1
    PERIOD_M5 = 5
    PERIOD_M15 = 15
    PERIOD_M30 = 30
    PERIOD_H1 = 60
    PERIOD_H4 = 240
    PERIOD_D1 = 1440
    PERIOD_W1 = 10080
    PERIOD_MN1 = 43200


@dataclass
class MT4Order:
    """MT4-style order definition."""

    symbol: str
    cmd: MT4OrderType
    volume: float  # Lots
    price: float
    slippage: int = 3
    stoploss: float = 0.0
    takeprofit: float = 0.0
    comment: str = ""
    magic: int = 0
    expiration: Optional[datetime] = None

    @classmethod
    def market_buy(cls, symbol: str, lots: float, sl: float = 0, tp: float = 0) -> "MT4Order":
        """Create a market buy order."""
        return cls(
            symbol=symbol,
            cmd=MT4OrderType.OP_BUY,
            volume=lots,
            price=0,  # Market orders use current price
            stoploss=sl,
            takeprofit=tp,
        )

    @classmethod
    def market_sell(cls, symbol: str, lots: float, sl: float = 0, tp: float = 0) -> "MT4Order":
        """Create a market sell order."""
        return cls(
            symbol=symbol,
            cmd=MT4OrderType.OP_SELL,
            volume=lots,
            price=0,
            stoploss=sl,
            takeprofit=tp,
        )


@dataclass
class MT4Tick:
    """MT4 tick data."""

    symbol: str
    time: datetime
    bid: float
    ask: float
    last: float
    volume: int


class SimulatedMT4(SimulatedAPI):
    """Simulated MetaTrader 4 API.

    Mimics the MT4 Python API interface for seamless transition between backtesting and live trading.
    """

    def __init__(self, action_collector: ActionCollector):
        """Initialize the simulated MT4 API."""
        super().__init__(action_collector)
        self._positions: Dict[str, Position] = {}
        self._account_info = {
            "balance": 10000.0,
            "equity": 10000.0,
            "margin": 0.0,
            "free_margin": 10000.0,
            "margin_level": 0.0,
            "profit": 0.0,
            "credit": 0.0,
            "leverage": 100,
        }
        self._next_ticket = 100000
        self._history_orders: List[Dict[str, Any]] = []
        self._open_orders: Dict[int, Dict[str, Any]] = {}

    def connect(self, **kwargs: Any) -> None:
        """Connect to MT4 server.

        Args:
            server: Server address (ignored in simulation)
            login: Account login (ignored in simulation)
            password: Account password (ignored in simulation)
            timeout: Connection timeout in ms (ignored in simulation)
        """
        server = kwargs.get("server", "")
        self.logger.info(f"Simulated connection to MT4 server: {server}")
        self._connected = True

        # Emit initial account update
        self.emit_account_update(self._account_info.copy())

    def disconnect(self) -> None:
        """Disconnect from MT4."""
        self.logger.info("Disconnecting from simulated MT4")
        self._connected = False
        self._subscribed_symbols.clear()

    def subscribe_market_data(self, symbols: List[str], **kwargs: Any) -> None:
        """Subscribe to market data for given symbols.

        Args:
            symbols: List of symbols to subscribe to
            **kwargs: Additional parameters (timeframe, etc.)
        """
        for symbol in symbols:
            self._subscribed_symbols.add(symbol)
            self.logger.info(f"Subscribed to MT4 market data for {symbol}")

    def symbol_subscribe(self, symbol: str, timeframe: MT4TimeFrame = MT4TimeFrame.PERIOD_M1) -> None:
        """Subscribe to a symbol (MT4-style method).

        Args:
            symbol: Symbol to subscribe to
            timeframe: Timeframe for subscription
        """
        self._subscribed_symbols.add(symbol)
        self.logger.info(f"Subscribed to {symbol} on {timeframe.name}")

    def place_order(self, order: Order) -> str:
        """Place an order (generic method).

        Args:
            order: Order to place

        Returns:
            Order ID (ticket number as string)
        """
        # Convert to MT4 order
        mt4_order = self._convert_to_mt4_order(order)

        # Get ticket number
        ticket = self._get_next_ticket()

        # Use action collector
        self.action_collector.add_order(
            symbol=order.symbol,
            side=order.side,
            quantity=order.quantity,
            order_type=order.order_type,
            price=order.price,
            additional_params={"mt4_ticket": str(ticket)},
        )

        self.logger.info(f"Placed MT4 order {ticket}: {mt4_order}")

        # Store order
        self._open_orders[ticket] = {
            "ticket": ticket,
            "symbol": order.symbol,
            "type": mt4_order.cmd.value,
            "volume": mt4_order.volume,
            "price": mt4_order.price,
            "sl": mt4_order.stoploss,
            "tp": mt4_order.takeprofit,
            "time": datetime.now(),
        }

        # Simulate immediate acknowledgment
        self.emit_order_update(str(ticket), "submitted")

        return str(ticket)

    def order_send(self, order: MT4Order) -> int:
        """Send an order (MT4-style method).

        Args:
            order: MT4 order to send

        Returns:
            Ticket number (0 on error)
        """
        ticket = self._get_next_ticket()

        # Convert to internal format
        side = "buy" if order.cmd in [MT4OrderType.OP_BUY, MT4OrderType.OP_BUYLIMIT, MT4OrderType.OP_BUYSTOP] else "sell"
        order_type = self._convert_mt4_order_type(order.cmd)

        self.action_collector.add_order(
            symbol=order.symbol,
            side=side,
            quantity=order.volume,
            order_type=order_type,
            price=order.price if order.price > 0 else None,
            additional_params={
                "mt4_ticket": str(ticket),
                "slippage": str(order.slippage),
                "sl": str(order.stoploss),
                "tp": str(order.takeprofit),
                "comment": order.comment,
                "magic": str(order.magic),
            },
        )

        # Store order
        self._open_orders[ticket] = {
            "ticket": ticket,
            "symbol": order.symbol,
            "type": order.cmd.value,
            "volume": order.volume,
            "price": order.price,
            "sl": order.stoploss,
            "tp": order.takeprofit,
            "comment": order.comment,
            "magic": order.magic,
            "time": datetime.now(),
        }

        self.logger.info(f"Sent MT4 order: ticket={ticket}")

        # Simulate acknowledgment
        self.emit_order_update(str(ticket), "submitted")

        return ticket

    def cancel_order(self, order_id: str) -> None:
        """Cancel an order.

        Args:
            order_id: Order ID (ticket) to cancel
        """
        self.action_collector.add_cancel_order(order_id)
        self.logger.info(f"Cancelled MT4 order {order_id}")

        # Remove from open orders
        ticket = int(order_id)
        if ticket in self._open_orders:
            order_info = self._open_orders.pop(ticket)
            order_info["close_time"] = datetime.now()
            self._history_orders.append(order_info)

        # Simulate cancellation
        self.emit_order_update(order_id, "cancelled")

    def order_close(self, ticket: int, volume: float = 0, price: float = 0, slippage: int = 3) -> bool:
        """Close an order (MT4-style method).

        Args:
            ticket: Order ticket to close
            volume: Volume to close (0 for full close)
            price: Close price (0 for market)
            slippage: Allowed slippage

        Returns:
            True if successful
        """
        self.cancel_order(str(ticket))
        return True

    def get_positions(self) -> Dict[str, Position]:
        """Get all open positions.

        Returns:
            Dictionary of symbol to position
        """
        return self._positions.copy()

    def positions_get(self, symbol: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get positions (MT4-style method).

        Args:
            symbol: Optional symbol filter

        Returns:
            List of position dictionaries
        """
        positions = []
        for sym, pos in self._positions.items():
            if symbol and sym != symbol:
                continue

            positions.append(
                {
                    "ticket": 0,  # Position ticket
                    "symbol": sym,
                    "type": 0 if pos.quantity > 0 else 1,  # Buy/Sell
                    "volume": abs(pos.quantity),
                    "price": pos.average_price,
                    "profit": pos.unrealized_pnl,
                    "swap": 0.0,
                    "commission": 0.0,
                    "comment": "",
                    "magic": 0,
                }
            )

        return positions

    def get_account_info(self) -> Dict[str, Any]:
        """Get account information.

        Returns:
            Dictionary of account values
        """
        return self._account_info.copy()

    def account_info(self) -> Dict[str, Any]:
        """Get account info (MT4-style method).

        Returns:
            Account information dictionary
        """
        return self._account_info.copy()

    def symbol_info(self, symbol: str) -> Dict[str, Any]:
        """Get symbol information.

        Args:
            symbol: Symbol to get info for

        Returns:
            Symbol information
        """
        # Return mock symbol info
        return {
            "symbol": symbol,
            "digits": 5 if "JPY" in symbol else 4,  # Forex convention
            "point": 0.00001 if "JPY" not in symbol else 0.001,
            "spread": 2,
            "stoplevel": 0,
            "lotsize": 100000,  # Standard lot
            "tickvalue": 1.0,
            "ticksize": 0.00001,
            "swaplong": -0.5,
            "swapshort": -0.3,
            "minvolume": 0.01,
            "maxvolume": 100.0,
            "volumestep": 0.01,
        }

    def _convert_to_mt4_order(self, order: Order) -> MT4Order:
        """Convert generic order to MT4 order.

        Args:
            order: Generic order

        Returns:
            MT4-style order
        """
        if order.side == "buy":
            if order.order_type == "market":
                cmd = MT4OrderType.OP_BUY
            elif order.order_type == "limit":
                cmd = MT4OrderType.OP_BUYLIMIT
            elif order.order_type == "stop":
                cmd = MT4OrderType.OP_BUYSTOP
            else:
                cmd = MT4OrderType.OP_BUY
        else:
            if order.order_type == "market":
                cmd = MT4OrderType.OP_SELL
            elif order.order_type == "limit":
                cmd = MT4OrderType.OP_SELLLIMIT
            elif order.order_type == "stop":
                cmd = MT4OrderType.OP_SELLSTOP
            else:
                cmd = MT4OrderType.OP_SELL

        return MT4Order(
            symbol=order.symbol,
            cmd=cmd,
            volume=order.quantity,
            price=order.price or 0,
        )

    def _convert_mt4_order_type(self, cmd: MT4OrderType) -> str:
        """Convert MT4 order type to generic type.

        Args:
            cmd: MT4 order type

        Returns:
            Generic order type
        """
        if cmd in [MT4OrderType.OP_BUY, MT4OrderType.OP_SELL]:
            return "market"
        elif cmd in [MT4OrderType.OP_BUYLIMIT, MT4OrderType.OP_SELLLIMIT]:
            return "limit"
        elif cmd in [MT4OrderType.OP_BUYSTOP, MT4OrderType.OP_SELLSTOP]:
            return "stop"
        else:
            return "market"

    def _get_next_ticket(self) -> int:
        """Get next ticket number.

        Returns:
            Next ticket number
        """
        ticket = self._next_ticket
        self._next_ticket += 1
        return ticket

    # Event callbacks MT4-style
    def onTick(self, callback: Callable) -> None:
        """Register callback for tick data.

        Args:
            callback: Callback function
        """

        def wrapper(data: MarketData) -> None:
            tick = MT4Tick(
                symbol=data.symbol,
                time=data.timestamp,
                bid=data.bid,
                ask=data.ask,
                last=data.last,
                volume=data.volume,
            )
            callback(tick)

        self.register_callback("market_data", wrapper)

    def onBar(self, callback: Callable) -> None:
        """Register callback for bar/candle data.

        Args:
            callback: Callback function
        """

        def wrapper(data: MarketData) -> None:
            if data.open is not None:  # It's a candle
                bar = {
                    "symbol": data.symbol,
                    "time": data.timestamp,
                    "open": data.open,
                    "high": data.high,
                    "low": data.low,
                    "close": data.close,
                    "volume": data.volume,
                }
                callback(bar)

        self.register_callback("market_data", wrapper)

    def onOrderEvent(self, callback: Callable) -> None:
        """Register callback for order events.

        Args:
            callback: Callback function
        """
        self.register_callback("order_update", callback)
