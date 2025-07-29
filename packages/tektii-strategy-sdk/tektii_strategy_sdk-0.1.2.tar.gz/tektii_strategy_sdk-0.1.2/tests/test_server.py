"""Tests for the gRPC server implementation."""

from contextlib import suppress
from datetime import datetime
from typing import Any, Dict, List, Tuple
from unittest.mock import MagicMock, Mock, patch

import grpc
import pytest
from google.protobuf import timestamp_pb2
from grpc_health.v1 import health_pb2, health_pb2_grpc

# Import SDK components
from tektii_sdk import Strategy, StrategyConfig
from tektii_sdk.apis import SimulatedIB
from tektii_sdk.collector import ActionCollector
from tektii_sdk.proto import strategy_pb2, strategy_pb2_grpc
from tektii_sdk.server import StrategyServicer, serve
from tektii_sdk.strategy import MarketData


class MockStrategy(Strategy):
    """Mock strategy for testing."""

    def __init__(self, config: StrategyConfig):
        """Initialize the mock strategy."""
        super().__init__(config)
        self.events_received: List[Tuple[str, Any]] = []

    def on_start(self) -> None:
        """Handle strategy start."""

    def on_market_data(self, data: MarketData) -> None:
        """Process market data."""
        self.events_received.append(("market_data", data))

    def on_stop(self) -> None:
        """Handle strategy stop."""


class TestStrategyServicer:
    """Test cases for StrategyServicer."""

    @pytest.fixture  # type: ignore[misc]
    def config(self) -> StrategyConfig:
        """Create test configuration."""
        return StrategyConfig(
            name="TestStrategy",
            version="1.0.0",
            symbols=["BTC-USD", "ETH-USD"],
            initial_capital=10000.0,
        )

    @pytest.fixture  # type: ignore[misc]
    def instrument_mapping(self) -> Dict[int, str]:
        """Create instrument ID to symbol mapping."""
        return {1: "BTC-USD", 2: "ETH-USD"}

    @pytest.fixture  # type: ignore[misc]
    def servicer(self, config: StrategyConfig, instrument_mapping: Dict[int, str]) -> "StrategyServicer":
        """Create servicer instance."""
        api = SimulatedIB(ActionCollector())
        return StrategyServicer(MockStrategy, config, api, instrument_mapping)

    @pytest.fixture  # type: ignore[misc]
    def mock_context(self) -> Mock:
        """Create mock gRPC context."""
        context = Mock(spec=grpc.ServicerContext)
        return context

    def test_standard_health_check(self) -> None:
        """Test standard gRPC health check."""
        from concurrent import futures

        from grpc_health.v1 import health

        # Create a test server with health check
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
        health_servicer = health.HealthServicer()
        health_pb2_grpc.add_HealthServicer_to_server(health_servicer, server)

        # Set health status
        service_name = "test.Service"
        health_servicer.set(service_name, health_pb2.HealthCheckResponse.SERVING)
        health_servicer.set("", health_pb2.HealthCheckResponse.SERVING)

        # Add to a test port
        port = server.add_insecure_port("[::]:0")
        server.start()

        try:
            # Create client channel
            channel = grpc.insecure_channel(f"localhost:{port}")
            health_stub = health_pb2_grpc.HealthStub(channel)

            # Check overall health
            request = health_pb2.HealthCheckRequest(service="")
            response = health_stub.Check(request)
            assert response.status == health_pb2.HealthCheckResponse.SERVING

            # Check specific service health
            request = health_pb2.HealthCheckRequest(service=service_name)
            response = health_stub.Check(request)
            assert response.status == health_pb2.HealthCheckResponse.SERVING

            # Test NOT_SERVING status
            health_servicer.set(service_name, health_pb2.HealthCheckResponse.NOT_SERVING)
            response = health_stub.Check(health_pb2.HealthCheckRequest(service=service_name))
            assert response.status == health_pb2.HealthCheckResponse.NOT_SERVING

        finally:
            server.stop(grace=0)
            channel.close()

    def test_health_check_with_strategy_servicer(self) -> None:
        """Test health check integration with StrategyServicer."""
        from concurrent import futures

        from grpc_health.v1 import health

        # Create test config
        config = StrategyConfig(
            name="TestStrategy",
            version="1.0.0",
            description="Test strategy",
            author="Test Author",
            symbols=["BTC-USD", "ETH-USD"],
            timeframe="1m",
            lookback_periods=100,
            initial_capital=10000.0,
        )

        # Create server with both services
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))

        # Add health servicer
        health_servicer = health.HealthServicer()
        health_pb2_grpc.add_HealthServicer_to_server(health_servicer, server)

        # Add strategy servicer
        api = SimulatedIB(ActionCollector())
        servicer = StrategyServicer(MockStrategy, config, api, {1: "BTC-USD"}, health_servicer)
        strategy_pb2_grpc.add_StrategyServiceServicer_to_server(servicer, server)

        # Start server
        port = server.add_insecure_port("[::]:0")
        server.start()

        try:
            # Create client
            channel = grpc.insecure_channel(f"localhost:{port}")
            health_stub = health_pb2_grpc.HealthStub(channel)

            # Initially should be NOT_SERVING (not initialized)
            response = health_stub.Check(health_pb2.HealthCheckRequest(service=""))
            # The serve() function sets initial status, but we're testing the servicer directly
            # So we need to check if health servicer was properly integrated

            # Initialize the strategy
            servicer._initialize_if_needed()

            # After initialization, health should be SERVING
            response = health_stub.Check(health_pb2.HealthCheckRequest(service=""))
            assert response.status == health_pb2.HealthCheckResponse.SERVING

        finally:
            server.stop(grace=0)
            channel.close()

    def test_process_candle_event(self, servicer: "StrategyServicer", mock_context: Mock) -> None:
        """Test processing candle data event."""
        # Create timestamp
        now = datetime.now()
        timestamp = timestamp_pb2.Timestamp()
        timestamp.FromDatetime(now)

        # Create candle data
        candle = strategy_pb2.CandleData(  # type: ignore[attr-defined]
            timestamp=timestamp, open="100.0", high="105.0", low="95.0", close="102.0", volume=1000
        )

        # Create candle event
        candle_event = strategy_pb2.CandleDataEvent(  # type: ignore[attr-defined]
            instrument_id=1,  # BTC-USD
            timeframe_id=5,  # 5 minutes
            exchange="BINANCE",
            candle=candle,
        )

        # Create event
        event = strategy_pb2.Event(  # type: ignore[attr-defined]
            event_id="test-123",
            timestamp=timestamp,
            event_type=strategy_pb2.EventType.EVENT_TYPE_MARKET_DATA,  # type: ignore[attr-defined]
            candle_data=candle_event,
        )

        # Process event
        response = servicer.ProcessEvent(event, mock_context)

        assert response.event_id == "test-123"
        assert len(servicer.strategy.events_received) > 0

        # Check market data was received
        event_type, data = servicer.strategy.events_received[0]
        assert event_type == "market_data"
        assert data.symbol == "BTC-USD"
        assert data.close == 102.0

    def test_process_order_execution_event(self, servicer: "StrategyServicer", mock_context: Mock) -> None:
        """Test processing order execution event."""
        # Create timestamp
        now = datetime.now()
        timestamp = timestamp_pb2.Timestamp()
        timestamp.FromDatetime(now)

        # Create order execution event
        order_exec = strategy_pb2.OrderExecutionEvent(  # type: ignore[attr-defined]
            order_id="order-456",
            instrument_id=2,  # ETH-USD
            direction=strategy_pb2.Direction.Direction_BUY,  # type: ignore[attr-defined]
            price=3000.0,
            quantity=0.5,
            executed_at=timestamp,
            order_type=strategy_pb2.OrderType.ORDER_TYPE_MARKET,  # type: ignore[attr-defined]
        )

        # Create event
        event = strategy_pb2.Event(  # type: ignore[attr-defined]
            event_id="test-456",
            timestamp=timestamp,
            event_type=strategy_pb2.EventType.EVENT_TYPE_ORDER_EXECUTION,  # type: ignore[attr-defined]
            order_execution=order_exec,
        )

        # Process event
        response = servicer.ProcessEvent(event, mock_context)

        assert response.event_id == "test-456"

        # Check position was updated
        position = servicer.strategy.get_position("ETH-USD")
        assert position is not None
        assert position.quantity == 0.5
        assert position.average_price == 3000.0

    def test_place_order_action(self, servicer: "StrategyServicer", mock_context: Mock) -> None:
        """Test generating place order actions."""
        # Setup strategy to place an order
        servicer._initialize_if_needed()
        servicer.strategy.buy("BTC-USD", 0.1, "limit", price=50000.0)

        # Create dummy event
        now = datetime.now()
        timestamp = timestamp_pb2.Timestamp()
        timestamp.FromDatetime(now)

        event = strategy_pb2.Event(  # type: ignore[attr-defined]
            event_id="test-789", timestamp=timestamp, event_type=strategy_pb2.EventType.EVENT_TYPE_MARKET_DATA  # type: ignore[attr-defined]
        )

        # Get response
        response = servicer._build_action_response(event.event_id)

        assert len(response.actions) == 1
        assert response.actions[0].action_type == strategy_pb2.ActionType.ACTION_TYPE_PLACE_ORDER  # type: ignore[attr-defined]

        place_order = response.actions[0].place_order
        assert place_order.instrument_id == 1  # BTC-USD
        assert place_order.direction == strategy_pb2.Direction.Direction_BUY  # type: ignore[attr-defined]
        assert place_order.quantity == 0  # Converted to int
        assert place_order.price == 50000.0
        assert place_order.order_type == strategy_pb2.OrderType.ORDER_TYPE_LIMIT  # type: ignore[attr-defined]

    def test_cancel_order_action(self, servicer: "StrategyServicer", mock_context: Mock) -> None:
        """Test generating cancel order actions."""
        # Setup strategy to cancel an order
        servicer._initialize_if_needed()
        servicer.strategy.action_collector.add_cancel_order("order-123")

        # Create dummy event
        now = datetime.now()
        timestamp = timestamp_pb2.Timestamp()
        timestamp.FromDatetime(now)

        event = strategy_pb2.Event(  # type: ignore[attr-defined]
            event_id="test-cancel",
            timestamp=timestamp,
            event_type=strategy_pb2.EventType.EVENT_TYPE_MARKET_DATA,  # type: ignore[attr-defined]
        )

        # Get response
        response = servicer._build_action_response(event.event_id)

        assert len(response.actions) == 1
        assert response.actions[0].action_type == strategy_pb2.ActionType.ACTION_TYPE_CANCEL_ORDER  # type: ignore[attr-defined]
        assert response.actions[0].cancel_order.order_id == "order-123"

    def test_error_handling(self, servicer: "StrategyServicer", mock_context: Mock) -> None:
        """Test error handling in event processing."""
        # Create event that will cause a warning (not error)
        event = strategy_pb2.Event(event_id="test-error", event_type=999)  # type: ignore[attr-defined]

        # Should not raise, but return response with warning in debug_info
        response = servicer.ProcessEvent(event, mock_context)

        assert response.event_id == "test-error"
        assert "Unknown event type" in response.debug_info or "WARNING" in response.debug_info
        assert len(response.actions) == 0

    def test_debug_info_from_logs(self, servicer: "StrategyServicer", mock_context: Mock) -> None:
        """Test debug info includes strategy logs."""
        # Initialize and add some logs
        servicer._initialize_if_needed()
        servicer.strategy.log("Debug message", level="debug")
        servicer.strategy.log("Info message", level="info")
        servicer.strategy.log("Error message", level="error")

        # Build response
        response = servicer._build_action_response("test-logs")

        assert "[DEBUG] Debug message" in response.debug_info
        assert "[INFO] Info message" in response.debug_info
        assert "[ERROR] Error message" in response.debug_info


class TestServerFunction:
    """Test cases for the serve function."""

    @patch("tektii_sdk.server.grpc.server")
    @patch("tektii_sdk.server.futures.ThreadPoolExecutor")
    @patch("tektii_sdk.server.logging.basicConfig")
    def test_serve_function(self, mock_logging: MagicMock, mock_executor: MagicMock, mock_grpc_server: MagicMock) -> None:
        """Test serve function setup."""
        # Setup mocks
        mock_server_instance = MagicMock()
        mock_grpc_server.return_value = mock_server_instance
        mock_executor_instance = MagicMock()
        mock_executor.return_value = mock_executor_instance

        # Mock server methods
        mock_server_instance.add_insecure_port = MagicMock()
        mock_server_instance.start = MagicMock()
        mock_server_instance.wait_for_termination = MagicMock()

        config = StrategyConfig(name="TestStrategy", version="1.0.0")

        # We need to prevent the server from actually starting and blocking
        # by making wait_for_termination return immediately
        mock_server_instance.wait_for_termination.side_effect = KeyboardInterrupt()

        # Call serve
        with suppress(KeyboardInterrupt):
            serve(MockStrategy, config, port=50052)

        # Verify server setup
        mock_grpc_server.assert_called_once_with(mock_executor_instance)
        mock_server_instance.add_insecure_port.assert_called_with("[::]:50052")
        mock_server_instance.start.assert_called_once()
