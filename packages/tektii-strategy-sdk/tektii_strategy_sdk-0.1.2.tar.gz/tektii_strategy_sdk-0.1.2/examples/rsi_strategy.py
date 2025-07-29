"""RSI Mean Reversion Strategy Example.

This example demonstrates a more advanced strategy using:
- Technical indicators (RSI)
- Multiple timeframes
- Position sizing based on signal strength
- Stop loss and take profit orders
- Risk management
"""

from collections import defaultdict, deque
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Deque, Dict, List, Optional, Tuple

from tektii_sdk import SimulatedIB, Strategy, StrategyConfig
from tektii_sdk.server import serve
from tektii_sdk.strategy import MarketData, Position, TimeFrame


@dataclass
class RSISignal:
    """RSI signal information."""

    symbol: str
    timestamp: datetime
    rsi_value: float
    signal_type: str  # "oversold", "overbought", "neutral"
    strength: float  # 0-1, how strong the signal is


class RSIStrategy(Strategy):
    """RSI-based mean reversion strategy.

    This strategy:
    - Calculates RSI for each symbol
    - Buys when RSI < oversold threshold (default 30)
    - Sells when RSI > overbought threshold (default 70)
    - Uses position sizing based on RSI extremity
    - Implements stop loss and take profit
    """

    def __init__(self, config: StrategyConfig):
        """Initialize the RSI strategy."""
        super().__init__(config)

        # Strategy parameters
        self.rsi_period = config.parameters.get("rsi_period", 14)
        self.oversold_level = config.parameters.get("oversold_level", 30)
        self.overbought_level = config.parameters.get("overbought_level", 70)
        self.base_position_size = config.parameters.get("base_position_size", 0.1)
        self.stop_loss_pct = config.parameters.get("stop_loss_pct", 0.02)
        self.take_profit_pct = config.parameters.get("take_profit_pct", 0.05)
        self.max_positions_per_symbol = config.parameters.get("max_positions_per_symbol", 1)

        # Price and indicator tracking
        self.price_history: Dict[str, Deque[float]] = {}
        self.rsi_values: Dict[str, Deque[float]] = {}
        self.gains_losses: Dict[str, Tuple[Deque[float], Deque[float]]] = {}

        # Position tracking
        self.open_positions: Dict[str, Dict[str, Any]] = defaultdict(dict)
        self.pending_orders: Dict[str, List[str]] = defaultdict(list)
        self.last_signal: Dict[str, RSISignal] = {}

        # Performance tracking
        self.trade_count = 0
        self.win_count = 0
        self.total_pnl = 0.0

        self.log(f"Initialized RSI Strategy - Period: {self.rsi_period}, " f"Oversold: {self.oversold_level}, Overbought: {self.overbought_level}")

    def on_start(self) -> None:
        """Initialize strategy components."""
        for symbol in self.config.symbols:
            self.price_history[symbol] = deque(maxlen=self.rsi_period + 1)
            self.rsi_values[symbol] = deque(maxlen=100)  # Keep last 100 RSI values
            self.gains_losses[symbol] = (
                deque(maxlen=self.rsi_period),  # Gains
                deque(maxlen=self.rsi_period),  # Losses
            )

        self.log("RSI Strategy started successfully")

    def on_market_data(self, data: MarketData) -> None:
        """Process new market data."""
        symbol = data.symbol

        if symbol not in self.config.symbols:
            return

        # Add price to history
        self.price_history[symbol].append(data.last)

        # Need enough data for RSI calculation
        if len(self.price_history[symbol]) < self.rsi_period + 1:
            return

        # Calculate RSI
        rsi = self._calculate_rsi(symbol)
        if rsi is None:
            return

        self.rsi_values[symbol].append(rsi)

        # Log RSI periodically
        if len(self.rsi_values[symbol]) % 20 == 0:
            self.log(f"{symbol}: Price={data.last:.2f}, RSI={rsi:.2f}", level="debug")

        # Generate and act on signals
        signal = self._generate_signal(symbol, rsi, data)
        if signal:
            self.last_signal[symbol] = signal
            self._process_signal(signal, data)

    def _calculate_rsi(self, symbol: str) -> Optional[float]:
        """Calculate RSI for a symbol.

        Args:
            symbol: Symbol to calculate RSI for

        Returns:
            RSI value or None if not enough data
        """
        prices = list(self.price_history[symbol])

        if len(prices) < self.rsi_period + 1:
            return None

        # Calculate price changes
        gains, losses = self.gains_losses[symbol]

        # First calculation
        if len(gains) == 0:
            for i in range(1, self.rsi_period + 1):
                change = prices[i] - prices[i - 1]
                if change > 0:
                    gains.append(change)
                    losses.append(0)
                else:
                    gains.append(0)
                    losses.append(abs(change))
        else:
            # Subsequent calculations - use last change only
            change = prices[-1] - prices[-2]
            if change > 0:
                gains.append(change)
                losses.append(0)
            else:
                gains.append(0)
                losses.append(abs(change))

        # Calculate average gain/loss
        avg_gain: float = sum(gains) / self.rsi_period
        avg_loss: float = sum(losses) / self.rsi_period

        if avg_loss == 0:
            return 100.0  # No losses means RSI = 100

        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))

        return rsi

    def _generate_signal(self, symbol: str, rsi: float, data: MarketData) -> Optional[RSISignal]:
        """Generate trading signal based on RSI.

        Args:
            symbol: Symbol
            rsi: Current RSI value
            data: Market data

        Returns:
            RSI signal or None
        """
        # Determine signal type
        if rsi < self.oversold_level:
            signal_type = "oversold"
            # Strength increases as RSI gets more extreme
            strength = (self.oversold_level - rsi) / self.oversold_level
        elif rsi > self.overbought_level:
            signal_type = "overbought"
            strength = (rsi - self.overbought_level) / (100 - self.overbought_level)
        else:
            signal_type = "neutral"
            strength = 0.0

        # Only return signal if it's strong enough
        if strength > 0.1:  # Minimum 10% strength
            return RSISignal(
                symbol=symbol,
                timestamp=data.timestamp,
                rsi_value=rsi,
                signal_type=signal_type,
                strength=min(strength, 1.0),
            )

        return None

    def _process_signal(self, signal: RSISignal, data: MarketData) -> None:
        """Process trading signal.

        Args:
            signal: RSI signal
            data: Market data
        """
        symbol = signal.symbol
        position = self.get_position(symbol)

        if signal.signal_type == "oversold" and not position:
            # Buy signal - enter long position
            self._enter_position(symbol, "buy", signal, data)

        elif signal.signal_type == "overbought":
            if position and position.quantity > 0:
                # Sell signal - exit long position
                self._exit_position(symbol, signal, data)
            elif not position:
                # Could implement short selling here
                pass

    def _enter_position(self, symbol: str, side: str, signal: RSISignal, data: MarketData) -> None:
        """Enter a new position.

        Args:
            symbol: Symbol to trade
            side: "buy" or "sell"
            signal: RSI signal
            data: Market data
        """
        # Check if we already have max positions for this symbol
        if len(self.open_positions.get(symbol, {})) >= self.max_positions_per_symbol:
            return

        # Calculate position size based on signal strength
        position_size = self.base_position_size * (1 + signal.strength * 0.5)

        # Place market order
        try:
            order_id = self.buy(symbol, position_size, "market")

            # Calculate stop loss and take profit levels
            if side == "buy":
                stop_loss = data.last * (1 - self.stop_loss_pct)
                take_profit = data.last * (1 + self.take_profit_pct)
            else:
                stop_loss = data.last * (1 + self.stop_loss_pct)
                take_profit = data.last * (1 - self.take_profit_pct)

            # Store position info
            self.open_positions[symbol][order_id] = {
                "entry_price": data.last,
                "entry_time": data.timestamp,
                "size": position_size,
                "side": side,
                "stop_loss": stop_loss,
                "take_profit": take_profit,
                "signal": signal,
            }

            self.log(
                f"ENTRY {side.upper()}: {symbol} at {data.last:.2f}, "
                f"Size: {position_size:.4f}, RSI: {signal.rsi_value:.2f}, "
                f"Strength: {signal.strength:.2%}, SL: {stop_loss:.2f}, TP: {take_profit:.2f}"
            )

            # Add metadata
            self.action_collector.add_metadata("entry_signal", f"{signal.signal_type}_{symbol}")
            self.action_collector.add_metadata("signal_strength", f"{signal.strength:.2f}")

        except Exception as e:
            self.log(f"Failed to enter position for {symbol}: {e}", level="error")

    def _exit_position(self, symbol: str, signal: RSISignal, data: MarketData) -> None:
        """Exit an existing position.

        Args:
            symbol: Symbol to exit
            signal: RSI signal
            data: Market data
        """
        position = self.get_position(symbol)
        if not position:
            return

        try:
            # Place market order to close
            self.sell(symbol, abs(position.quantity), "market")

            # Calculate P&L
            pnl = position.unrealized_pnl
            self.total_pnl += pnl
            self.trade_count += 1
            if pnl > 0:
                self.win_count += 1

            win_rate = (self.win_count / self.trade_count * 100) if self.trade_count > 0 else 0

            self.log(
                f"EXIT: {symbol} at {data.last:.2f}, "
                f"P&L: {pnl:.2f}, RSI: {signal.rsi_value:.2f}, "
                f"Total P&L: {self.total_pnl:.2f}, Win Rate: {win_rate:.1f}%"
            )

            # Clean up position tracking
            self.open_positions[symbol].clear()

            # Add metadata
            self.action_collector.add_metadata("exit_signal", f"{signal.signal_type}_{symbol}")
            self.action_collector.add_metadata("trade_pnl", f"{pnl:.2f}")
            self.action_collector.add_metadata("total_pnl", f"{self.total_pnl:.2f}")

        except Exception as e:
            self.log(f"Failed to exit position for {symbol}: {e}", level="error")

    def on_position_update(self, position: Position) -> None:
        """Handle position updates."""
        super().on_position_update(position)

        # Check stop loss and take profit
        if position.symbol in self.open_positions:
            for _order_id, pos_info in self.open_positions[position.symbol].items():
                if position.quantity > 0:  # Long position
                    if position.current_price <= pos_info["stop_loss"]:
                        self.log(f"STOP LOSS triggered for {position.symbol} at {position.current_price:.2f}")
                        self._exit_position(
                            position.symbol,
                            RSISignal(position.symbol, datetime.now(), 0, "stop_loss", 1.0),
                            MarketData(
                                position.symbol,
                                datetime.now(),
                                position.current_price,
                                position.current_price,
                                position.current_price,
                                0,
                            ),
                        )
                    elif position.current_price >= pos_info["take_profit"]:
                        self.log(f"TAKE PROFIT triggered for {position.symbol} at {position.current_price:.2f}")
                        self._exit_position(
                            position.symbol,
                            RSISignal(position.symbol, datetime.now(), 0, "take_profit", 1.0),
                            MarketData(
                                position.symbol,
                                datetime.now(),
                                position.current_price,
                                position.current_price,
                                position.current_price,
                                0,
                            ),
                        )

    def on_stop(self) -> None:
        """Handle strategy stop.

        This method is called when the strategy is stopped, allowing for cleanup and final actions.
        """
        # Close all open positions
        for symbol in list(self.open_positions.keys()):
            position = self.get_position(symbol)
            if position and position.quantity != 0:
                self.log(f"Closing position on shutdown: {symbol}")
                if position.quantity > 0:
                    self.sell(symbol, position.quantity, "market")
                else:
                    self.buy(symbol, abs(position.quantity), "market")

        # Log final statistics
        win_rate = (self.win_count / self.trade_count * 100) if self.trade_count > 0 else 0
        self.log(f"Strategy stopped. Total trades: {self.trade_count}, " f"Win rate: {win_rate:.1f}%, Total P&L: {self.total_pnl:.2f}")


def main() -> None:
    """Initialize the RSI strategy example.

    This function sets up the strategy configuration, creates an instance of the strategy,
    and starts the server to handle incoming requests.
    """
    config = StrategyConfig(
        name="RSIStrategy",
        version="1.0.0",
        symbols=["BTC-USD", "ETH-USD"],
        timeframes=[TimeFrame.M5],
        initial_capital=100000.0,
        max_positions=2,
        risk_per_trade=0.02,
        parameters={
            "rsi_period": 14,
            "oversold_level": 30,
            "overbought_level": 70,
            "base_position_size": 0.1,
            "stop_loss_pct": 0.02,
            "take_profit_pct": 0.05,
            "max_positions_per_symbol": 1,
        },
    )

    # Instrument mapping
    instrument_mapping: Dict[int, str] = {
        1: "BTC-USD",
        2: "ETH-USD",
    }

    # Create API
    temp_strategy = RSIStrategy(config)
    api = SimulatedIB(temp_strategy.action_collector)

    serve(
        strategy_class=RSIStrategy,
        config=config,
        api=api,
        instrument_mapping=instrument_mapping,
        port=50051,
    )


if __name__ == "__main__":
    main()
