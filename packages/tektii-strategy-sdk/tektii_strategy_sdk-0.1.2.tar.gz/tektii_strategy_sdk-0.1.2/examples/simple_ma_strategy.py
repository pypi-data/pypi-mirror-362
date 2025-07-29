"""Simple Moving Average Crossover Strategy Example.

This example demonstrates how to build a basic trading strategy using the
tektii-strategy-sdk. The strategy uses two moving averages and generates
buy/sell signals when they cross.
"""

from collections import deque
from typing import Deque, Dict

from tektii_sdk import SimulatedIB, Strategy, StrategyConfig
from tektii_sdk.server import serve
from tektii_sdk.strategy import MarketData, Position, TimeFrame


class SimpleMAStrategy(Strategy):
    """Simple moving average crossover strategy.

    This strategy:
    - Tracks two moving averages (fast and slow)
    - Buys when fast MA crosses above slow MA
    - Sells when fast MA crosses below slow MA
    - Maintains only one position per symbol at a time
    """

    def __init__(self, config: StrategyConfig):
        """Initialize the strategy."""
        super().__init__(config)

        # Get MA periods from config
        self.fast_period = config.parameters.get("fast_period", 10)
        self.slow_period = config.parameters.get("slow_period", 20)
        self.position_size = config.parameters.get("position_size", 100)

        # Price history for each symbol
        self.price_history: Dict[str, Deque[float]] = {}

        # Moving averages
        self.fast_ma: Dict[str, float] = {}
        self.slow_ma: Dict[str, float] = {}

        # Track if we're in a position
        self.in_position: Dict[str, bool] = {}

        self.log(f"Initialized MA Strategy - Fast: {self.fast_period}, Slow: {self.slow_period}")

    def on_start(self) -> None:
        """Call when the strategy starts."""
        # Initialize data structures for each symbol
        for symbol in self.config.symbols:
            self.price_history[symbol] = deque(maxlen=self.slow_period)
            self.fast_ma[symbol] = 0.0
            self.slow_ma[symbol] = 0.0
            self.in_position[symbol] = False

        self.log("Strategy started successfully")

    def on_market_data(self, data: MarketData) -> None:
        """Process new market data."""
        symbol = data.symbol

        # Skip if not a symbol we're tracking
        if symbol not in self.config.symbols:
            return

        # Add price to history
        self.price_history[symbol].append(data.last)

        # Need enough data for slow MA
        if len(self.price_history[symbol]) < self.slow_period:
            return

        # Calculate moving averages
        prices = list(self.price_history[symbol])
        self.fast_ma[symbol] = sum(prices[-self.fast_period :]) / self.fast_period
        self.slow_ma[symbol] = sum(prices) / self.slow_period

        # Log current state periodically
        if len(self.price_history[symbol]) % 20 == 0:
            self.log(
                f"{symbol}: Price={data.last:.2f}, " f"Fast MA={self.fast_ma[symbol]:.2f}, " f"Slow MA={self.slow_ma[symbol]:.2f}",
                level="debug",
            )

        # Check for signals
        self._check_signals(symbol, data)

    def _check_signals(self, symbol: str, data: MarketData) -> None:
        """Check for trading signals."""
        # Need at least 2 data points to detect crossover
        if len(self.price_history[symbol]) < self.slow_period + 1:
            return

        # Get previous MAs (calculate from history minus last price)
        prev_prices = list(self.price_history[symbol])[:-1]
        prev_fast_ma = sum(prev_prices[-self.fast_period :]) / self.fast_period
        prev_slow_ma = sum(prev_prices[-self.slow_period :]) / self.slow_period

        # Current MAs
        curr_fast_ma = self.fast_ma[symbol]
        curr_slow_ma = self.slow_ma[symbol]

        # Check for crossover
        if prev_fast_ma <= prev_slow_ma and curr_fast_ma > curr_slow_ma:
            # Golden cross - buy signal
            if not self.in_position[symbol]:
                self._enter_long_position(symbol, data)

        elif prev_fast_ma >= prev_slow_ma and curr_fast_ma < curr_slow_ma and self.in_position[symbol]:
            # Death cross - sell signal
            self._exit_position(symbol, data)

    def _enter_long_position(self, symbol: str, data: MarketData) -> None:
        """Enter a long position."""
        try:
            self.buy(symbol, self.position_size, "market")
            self.in_position[symbol] = True

            self.log(f"BUY SIGNAL: {symbol} at {data.last:.2f} " f"(Fast MA: {self.fast_ma[symbol]:.2f} > Slow MA: {self.slow_ma[symbol]:.2f})")

            # Add metadata for analysis
            self.action_collector.add_metadata("last_signal", f"buy_{symbol}")
            self.action_collector.add_metadata("signal_price", str(data.last))

        except Exception as e:
            self.log(f"Failed to enter position for {symbol}: {e}", level="error")

    def _exit_position(self, symbol: str, data: MarketData) -> None:
        """Exit position."""
        try:
            # Get current position
            position = self.get_position(symbol)
            if position:
                self.sell(symbol, position.quantity, "market")
                self.in_position[symbol] = False

                self.log(
                    f"SELL SIGNAL: {symbol} at {data.last:.2f} "
                    f"(Fast MA: {self.fast_ma[symbol]:.2f} < Slow MA: {self.slow_ma[symbol]:.2f}), "
                    f"PnL: {position.unrealized_pnl:.2f}"
                )

                # Add metadata
                self.action_collector.add_metadata("last_signal", f"sell_{symbol}")
                self.action_collector.add_metadata("signal_price", str(data.last))
                self.action_collector.add_metadata("pnl", str(position.unrealized_pnl))

        except Exception as e:
            self.log(f"Failed to exit position for {symbol}: {e}", level="error")

    def on_position_update(self, position: Position) -> None:
        """Handle position updates."""
        super().on_position_update(position)

        # Update our position tracking
        if position.quantity > 0:
            self.in_position[position.symbol] = True
        else:
            self.in_position[position.symbol] = False

    def on_stop(self) -> None:
        """Call when the strategy stops."""
        # Close any open positions
        for symbol, in_pos in self.in_position.items():
            if in_pos:
                position = self.get_position(symbol)
                if position:
                    self.log(f"Closing position on shutdown: {symbol}, PnL: {position.unrealized_pnl:.2f}")
                    self.sell(symbol, position.quantity, "market")

        self.log("Strategy stopped")


def main() -> None:
    """Run the strategy.

    This can be run directly or via the CLI:

    Direct:
        python simple_ma_strategy.py

    Via CLI:
        tektii simple_ma_strategy.py SimpleMAStrategy --config ma_config.json
    """
    # Create strategy configuration
    config = StrategyConfig(
        name="SimpleMA",
        version="1.0.0",
        symbols=["BTC-USD", "ETH-USD"],  # Crypto pairs for demo
        timeframes=[TimeFrame.M5],  # 5-minute bars
        initial_capital=100000.0,
        max_positions=2,
        risk_per_trade=0.02,
        parameters={
            "fast_period": 10,
            "slow_period": 20,
            "position_size": 0.1,  # 0.1 BTC/ETH per trade
        },
    )

    # Instrument mapping (instrument_id -> symbol)
    # In production, this would come from the backtest engine
    instrument_mapping: Dict[int, str] = {
        1: "BTC-USD",
        2: "ETH-USD",
    }

    # Create simulated IB API
    # Temporary strategy instance to get action collector
    temp_strategy = SimpleMAStrategy(config)
    api = SimulatedIB(temp_strategy.action_collector)

    serve(
        strategy_class=SimpleMAStrategy,
        config=config,
        api=api,
        instrument_mapping=instrument_mapping,
        port=50051,
    )


if __name__ == "__main__":
    main()
