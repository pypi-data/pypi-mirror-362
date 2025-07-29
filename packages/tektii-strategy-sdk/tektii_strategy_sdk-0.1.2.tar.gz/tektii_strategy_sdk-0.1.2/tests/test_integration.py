"""Integration tests for the complete backtest SDK flow."""

from datetime import datetime
from typing import Dict, List, Tuple

import pytest

from tektii_sdk import Strategy, StrategyConfig
from tektii_sdk.strategy import MarketData

# Import proto files if available
try:
    from google.protobuf import timestamp_pb2

    from tektii_sdk.proto import strategy_pb2
    from tektii_sdk.server import StrategyServicer

    PROTO_AVAILABLE = True
except ImportError:
    PROTO_AVAILABLE = False
    strategy_pb2 = None  # type: ignore[assignment]


class IntegrationTestStrategy(Strategy):
    """Test strategy for integration testing."""

    def __init__(self, config: StrategyConfig):
        """Initialize the strategy with a configuration."""
        super().__init__(config)
        self.events: List[Tuple[str, MarketData]] = []
        self.trades: List[Tuple[str, str, float, str]] = []

    def on_start(self) -> None:
        """Handle strategy start."""
        self.log("Strategy started")

    def on_market_data(self, data: MarketData) -> None:
        """Process incoming market data."""
        self.events.append(("market_data", data))

        # Simple logic: buy if price < 100, sell if price > 110
        position = self.get_position(data.symbol)

        if data.last < 100 and not position:
            order_id = self.buy(data.symbol, 10, "limit", price=data.last)
            self.trades.append(("buy", data.symbol, data.last, order_id))
        elif data.last > 110 and position:
            order_id = self.sell(data.symbol, position.quantity, "market")
            self.trades.append(("sell", data.symbol, data.last, order_id))

    def on_stop(self) -> None:
        """Handle strategy stop."""
        self.log("Strategy stopped")


@pytest.mark.integration
class TestIntegration:
    """Integration tests."""

    def test_complete_flow(self) -> None:
        """Test complete flow from configuration to action collection."""
        # Create configuration
        config = StrategyConfig(
            name="IntegrationTest",
            version="1.0.0",
            symbols=["TEST1", "TEST2"],
            initial_capital=10000.0,
            parameters={"threshold": 100},
        )

        # Create strategy
        strategy = IntegrationTestStrategy(config)
        strategy.initialize()

        # Simulate market data
        data1 = MarketData(symbol="TEST1", timestamp=datetime.now(), bid=99.5, ask=99.6, last=99.5, volume=1000)

        strategy.emit_market_data(data1)

        # Check that strategy received data
        assert len(strategy.events) == 1
        assert strategy.events[0][0] == "market_data"

        # Check that order was placed
        assert len(strategy.trades) == 1
        assert strategy.trades[0][0] == "buy"

        # Check action collector
        orders = strategy.action_collector.get_orders()
        assert len(orders) == 1
        assert orders[0].symbol == "TEST1"
        assert orders[0].side == "buy"
        assert orders[0].order_type == "limit"
        assert orders[0].price == 99.5

    def test_stop_order_flow(self) -> None:
        """Test stop order handling."""
        config = StrategyConfig(name="StopTest", version="1.0.0")
        strategy = IntegrationTestStrategy(config)
        strategy.initialize()

        # Place a stop order
        strategy.buy("TEST1", 10, "stop", price=105.0)

        # Verify in action collector
        orders = strategy.action_collector.get_orders()
        assert len(orders) == 1
        assert orders[0].order_type == "stop"
        assert orders[0].stop_price == 105.0  # Price converted to stop_price

    def test_grpc_integration(self) -> None:
        """Test gRPC server integration."""
        # Create servicer
        config = StrategyConfig(name="GRPCTest", version="1.0.0", symbols=["BTC-USD"])

        instrument_mapping: Dict[int, str] = {1: "BTC-USD"}
        servicer = StrategyServicer(IntegrationTestStrategy, config, None, instrument_mapping)

        # Create a market data event
        now = datetime.now()
        timestamp = timestamp_pb2.Timestamp()
        timestamp.FromDatetime(now)

        candle = strategy_pb2.CandleData(  # type: ignore[attr-defined]
            timestamp=timestamp, open="99.0", high="100.0", low="98.0", close="99.5", volume=1000
        )

        candle_event = strategy_pb2.CandleDataEvent(instrument_id=1, timeframe_id=5, exchange="TEST", candle=candle)  # type: ignore[attr-defined]

        event = strategy_pb2.Event(  # type: ignore[attr-defined]
            event_id="test-001",
            timestamp=timestamp,
            event_type=strategy_pb2.EventType.EVENT_TYPE_MARKET_DATA,  # type: ignore[attr-defined]
            candle_data=candle_event,
        )

        # Process event
        response = servicer.ProcessEvent(event, None)

        # Check response
        assert response.event_id == "test-001"
        assert len(response.actions) == 1  # Should have placed an order
        assert response.actions[0].action_type == strategy_pb2.ActionType.ACTION_TYPE_PLACE_ORDER  # type: ignore[attr-defined]

    def test_error_recovery(self) -> None:
        """Test error handling and recovery."""
        config = StrategyConfig(name="ErrorTest", version="1.0.0")

        class ErrorStrategy(Strategy):
            def on_start(self) -> None:
                pass

            def on_market_data(self, data: MarketData) -> None:
                if data.symbol == "ERROR":
                    raise ValueError("Test error")
                self.buy(data.symbol, 10)

        strategy = ErrorStrategy(config)
        strategy.initialize()

        # This should not crash
        error_data = MarketData(symbol="ERROR", timestamp=datetime.now(), bid=100, ask=100, last=100, volume=1000)
        strategy.emit_market_data(error_data)

        # Should have logged the error
        logs = strategy.action_collector.get_logs()
        assert any("Error in strategy" in log.message for log in logs)

        # Strategy should still work for other symbols
        good_data = MarketData(symbol="GOOD", timestamp=datetime.now(), bid=100, ask=100, last=100, volume=1000)
        strategy.emit_market_data(good_data)

        # Should have placed an order
        orders = strategy.action_collector.get_orders()
        assert len(orders) == 1
        assert orders[0].symbol == "GOOD"
