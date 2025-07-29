"""Tests for the Strategy base class."""

from datetime import datetime
from typing import List

import pytest

from tektii_sdk import Strategy, StrategyConfig
from tektii_sdk.exceptions import StrategyError
from tektii_sdk.strategy import MarketData, Order, Position, TimeFrame


class TestStrategy(Strategy):
    """Test implementation of Strategy."""

    def __init__(self, config: StrategyConfig):
        """Initialize test strategy."""
        super().__init__(config)
        self.on_start_called = False
        self.on_stop_called = False
        self.market_data_received: List[MarketData] = []

    def on_start(self) -> None:
        """Handle strategy start."""
        self.on_start_called = True

    def on_market_data(self, data: MarketData) -> None:
        """Handle incoming market data."""
        self.market_data_received.append(data)

    def on_stop(self) -> None:
        """Handle strategy stop."""
        self.on_stop_called = True


class TestStrategyBase:
    """Test cases for Strategy base class."""

    @pytest.fixture  # type: ignore[misc]
    def config(self) -> StrategyConfig:
        """Create test configuration."""
        return StrategyConfig(
            name="TestStrategy",
            version="1.0.0",
            symbols=["AAPL", "GOOGL"],
            timeframes=[TimeFrame.M5],
            initial_capital=10000.0,
            max_positions=2,
            parameters={"test_param": 123},
        )

    @pytest.fixture  # type: ignore[misc]
    def strategy(self, config: StrategyConfig) -> TestStrategy:
        """Create test strategy instance."""
        return TestStrategy(config)

    def test_initialization(self, strategy: TestStrategy, config: StrategyConfig) -> None:
        """Test strategy initialization."""
        assert strategy.config == config
        assert strategy.action_collector is not None
        assert strategy._positions == {}
        assert strategy._pending_orders == {}
        assert not strategy._initialized

    def test_initialize(self, strategy: TestStrategy) -> None:
        """Test strategy initialization lifecycle."""
        strategy.initialize()

        assert strategy.on_start_called
        assert strategy._initialized

        # Should not re-initialize
        strategy.on_start_called = False
        strategy.initialize()
        assert not strategy.on_start_called

    def test_shutdown(self, strategy: TestStrategy) -> None:
        """Test strategy shutdown lifecycle."""
        strategy.initialize()
        strategy.shutdown()

        assert strategy.on_stop_called
        assert not strategy._initialized

    def test_emit_market_data(self, strategy: TestStrategy) -> None:
        """Test market data emission."""
        strategy.initialize()

        data = MarketData(
            symbol="AAPL",
            timestamp=datetime.now(),
            bid=150.0,
            ask=150.1,
            last=150.05,
            volume=1000000,
        )

        strategy.emit_market_data(data)

        assert len(strategy.market_data_received) == 1
        assert strategy.market_data_received[0] == data

    def test_buy_order(self, strategy: TestStrategy) -> None:
        """Test placing a buy order."""
        strategy.initialize()

        order_id = strategy.buy("AAPL", 100, "market")

        assert order_id is not None
        assert len(strategy._pending_orders) == 1

        orders = strategy.action_collector.get_orders()
        assert len(orders) == 1
        assert orders[0].symbol == "AAPL"
        assert orders[0].side == "buy"
        assert orders[0].quantity == 100
        assert orders[0].order_type == "market"

    def test_sell_order(self, strategy: TestStrategy) -> None:
        """Test placing a sell order."""
        strategy.initialize()

        order_id = strategy.sell("AAPL", 50, "limit", price=155.0)

        assert order_id is not None

        orders = strategy.action_collector.get_orders()
        assert len(orders) == 1
        assert orders[0].symbol == "AAPL"
        assert orders[0].side == "sell"
        assert orders[0].quantity == 50
        assert orders[0].order_type == "limit"
        assert orders[0].price == 155.0

    def test_stop_order(self, strategy: TestStrategy) -> None:
        """Test placing a stop order."""
        strategy.initialize()

        # Stop buy order
        order_id = strategy.buy("AAPL", 100, "stop", price=160.0)

        assert order_id is not None

        orders = strategy.action_collector.get_orders()
        assert len(orders) == 1
        assert orders[0].symbol == "AAPL"
        assert orders[0].side == "buy"
        assert orders[0].quantity == 100
        assert orders[0].order_type == "stop"
        assert orders[0].stop_price == 160.0  # Price becomes stop_price for stop orders

    def test_cancel_order(self, strategy: TestStrategy) -> None:
        """Test canceling an order."""
        strategy.initialize()

        order_id = strategy.buy("AAPL", 100, "limit", price=150.0)
        strategy.action_collector.clear()  # Clear the buy action

        strategy.cancel_order(order_id)

        assert order_id not in strategy._pending_orders

        orders = strategy.action_collector.get_orders()
        assert len(orders) == 1
        assert orders[0].action_type.value == "cancel_order"
        assert orders[0].order_id == order_id

    def test_position_management(self, strategy: TestStrategy) -> None:
        """Test position tracking."""
        strategy.initialize()

        # No position initially
        assert strategy.get_position("AAPL") is None

        # Add position
        position = Position(symbol="AAPL", quantity=100, average_price=150.0, current_price=155.0)
        strategy.on_position_update(position)

        # Check position
        retrieved = strategy.get_position("AAPL")
        assert retrieved == position
        assert retrieved.unrealized_pnl == 500.0  # (155-150) * 100

        # Get all positions
        all_positions = strategy.get_all_positions()
        assert len(all_positions) == 1
        assert all_positions["AAPL"] == position

    def test_max_positions_validation(self, strategy: TestStrategy) -> None:
        """Test max positions validation."""
        strategy.initialize()

        # Add positions up to max
        for _i, symbol in enumerate(["AAPL", "GOOGL"]):
            position = Position(symbol=symbol, quantity=100, average_price=100.0, current_price=100.0)
            strategy._positions[symbol] = position

        # Try to add position for new symbol - should fail
        with pytest.raises(StrategyError):
            strategy.buy("MSFT", 100, "market")

        # But can add to existing position
        order_id = strategy.buy("AAPL", 50, "market")
        assert order_id is not None

    def test_logging(self, strategy: TestStrategy) -> None:
        """Test strategy logging."""
        strategy.initialize()

        strategy.log("Test message", level="info")
        strategy.log("Error message", level="error")

        logs = strategy.action_collector.get_logs()
        assert len(logs) == 2
        assert logs[0].message == "Test message"
        assert logs[0].level.value == "info"
        assert logs[1].message == "Error message"
        assert logs[1].level.value == "error"

    def test_market_data_callbacks(self, strategy: TestStrategy) -> None:
        """Test registering market data callbacks."""
        strategy.initialize()

        callback_data: List[MarketData] = []

        def custom_callback(data: MarketData) -> None:
            callback_data.append(data)

        strategy.register_market_data_callback(custom_callback)

        # Emit data
        data = MarketData(
            symbol="AAPL",
            timestamp=datetime.now(),
            bid=150.0,
            ask=150.1,
            last=150.05,
            volume=1000000,
        )
        strategy.emit_market_data(data)

        # Both strategy and custom callback should receive data
        assert len(strategy.market_data_received) == 1
        assert len(callback_data) == 1
        assert callback_data[0] == data

    def test_order_validation(self, strategy: TestStrategy) -> None:
        """Test order validation."""
        # Test invalid side
        with pytest.raises(ValueError, match="Invalid order side"):
            Order(symbol="AAPL", side="invalid", quantity=100)

        # Test invalid quantity
        with pytest.raises(ValueError, match="quantity must be positive"):
            Order(symbol="AAPL", side="buy", quantity=0)

        with pytest.raises(ValueError, match="quantity must be positive"):
            Order(symbol="AAPL", side="buy", quantity=-10)

        # Test limit order without price
        with pytest.raises(ValueError, match="Price required"):
            Order(symbol="AAPL", side="buy", quantity=100, order_type="limit")

        # Test stop order without price
        with pytest.raises(ValueError, match="Price required"):
            Order(symbol="AAPL", side="buy", quantity=100, order_type="stop")

        # Test invalid order type
        with pytest.raises(ValueError, match="Invalid order type"):
            Order(symbol="AAPL", side="buy", quantity=100, order_type="invalid")

        # Valid orders should work
        order = Order(symbol="AAPL", side="buy", quantity=100, order_type="market")
        assert order is not None

        order = Order(symbol="AAPL", side="sell", quantity=100, order_type="limit", price=150.0)
        assert order is not None

        order = Order(symbol="AAPL", side="buy", quantity=100, order_type="stop", price=160.0)
        assert order is not None


class TestMarketData:
    """Test cases for MarketData class."""

    def test_market_data_properties(self) -> None:
        """Test MarketData calculated properties."""
        data = MarketData(
            symbol="EURUSD",
            timestamp=datetime.now(),
            bid=1.1000,
            ask=1.1002,
            last=1.1001,
            volume=1000000,
        )

        assert data.mid == 1.1001
        assert data.spread == pytest.approx(0.0002)

    def test_market_data_with_ohlc(self) -> None:
        """Test MarketData with OHLC data."""
        data = MarketData(
            symbol="AAPL",
            timestamp=datetime.now(),
            bid=150.0,
            ask=150.1,
            last=150.05,
            volume=1000000,
            timeframe=TimeFrame.M5,
            open=149.0,
            high=150.5,
            low=148.5,
            close=150.05,
        )

        assert data.open == 149.0
        assert data.high == 150.5
        assert data.low == 148.5
        assert data.close == 150.05
        assert data.timeframe == TimeFrame.M5


class TestPosition:
    """Test cases for Position class."""

    def test_position_pnl_calculation(self) -> None:
        """Test position P&L calculation."""
        position = Position(symbol="AAPL", quantity=100, average_price=150.0, current_price=155.0)

        assert position.unrealized_pnl == 500.0

        # Update price
        position.update_pnl(160.0)
        assert position.current_price == 160.0
        assert position.unrealized_pnl == 1000.0

        # Short position
        short_position = Position(symbol="AAPL", quantity=-100, average_price=150.0, current_price=145.0)

        assert short_position.unrealized_pnl == 500.0  # Profit on short
