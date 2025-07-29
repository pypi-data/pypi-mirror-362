"""Tests for the ActionCollector class."""

import pytest

from tektii_sdk.collector import ActionCollector, ActionType, LogEntry, LogLevel, OrderAction


class TestActionCollector:
    """Test cases for ActionCollector."""

    @pytest.fixture  # type: ignore[misc]
    def collector(self) -> ActionCollector:
        """Create a fresh ActionCollector instance."""
        return ActionCollector()

    def test_initialization(self, collector: ActionCollector) -> None:
        """Test collector initializes empty."""
        assert len(collector.get_orders()) == 0
        assert len(collector.get_logs()) == 0
        assert len(collector.get_metadata()) == 0

    def test_add_order(self, collector: ActionCollector) -> None:
        """Test adding a place order action."""
        order_id = collector.add_order(symbol="AAPL", side="buy", quantity=100, order_type="limit", price=150.0)

        assert order_id is not None
        assert order_id.startswith("ORD-")

        orders = collector.get_orders()
        assert len(orders) == 1

        order = orders[0]
        assert order.action_type == ActionType.PLACE_ORDER
        assert order.symbol == "AAPL"
        assert order.side == "buy"
        assert order.quantity == 100
        assert order.order_type == "limit"
        assert order.price == 150.0
        assert order.order_id == order_id

    def test_add_stop_order(self, collector: ActionCollector) -> None:
        """Test adding a stop order."""
        collector.add_order(symbol="AAPL", side="sell", quantity=50, order_type="stop", price=140.0)  # Stop price

        orders = collector.get_orders()
        assert len(orders) == 1

        order = orders[0]
        assert order.action_type == ActionType.PLACE_ORDER
        assert order.order_type == "stop"
        assert order.stop_price == 140.0  # Price is converted to stop_price for stop orders

    def test_add_cancel_order(self, collector: ActionCollector) -> None:
        """Test adding a cancel order action."""
        collector.add_cancel_order("ORDER-123")

        orders = collector.get_orders()
        assert len(orders) == 1

        order = orders[0]
        assert order.action_type == ActionType.CANCEL_ORDER
        assert order.order_id == "ORDER-123"

    def test_add_modify_order(self, collector: ActionCollector) -> None:
        """Test adding a modify order action."""
        collector.add_modify_order(order_id="ORDER-456", quantity=200, price=155.0)

        orders = collector.get_orders()
        assert len(orders) == 1

        order = orders[0]
        assert order.action_type == ActionType.MODIFY_ORDER
        assert order.order_id == "ORDER-456"
        assert order.additional_params["new_quantity"] == 200
        assert order.additional_params["new_price"] == 155.0

    def test_add_log(self, collector: ActionCollector) -> None:
        """Test adding log entries."""
        collector.add_log("Test message", "info")
        collector.add_log("Error message", "error")

        logs = collector.get_logs()
        assert len(logs) == 2

        assert logs[0].message == "Test message"
        assert logs[0].level == LogLevel.INFO

        assert logs[1].message == "Error message"
        assert logs[1].level == LogLevel.ERROR

    def test_add_metadata(self, collector: ActionCollector) -> None:
        """Test adding metadata."""
        collector.add_metadata("strategy", "MA_Crossover")
        collector.add_metadata("version", "1.0.0")

        metadata = collector.get_metadata()
        assert len(metadata) == 2
        assert metadata["strategy"] == "MA_Crossover"
        assert metadata["version"] == "1.0.0"

    def test_clear(self, collector: ActionCollector) -> None:
        """Test clearing all collected actions."""
        # Add some data
        collector.add_order("AAPL", "buy", 100)
        collector.add_log("Test log", "info")
        collector.add_metadata("key", "value")

        # Verify data exists
        assert len(collector.get_orders()) == 1
        assert len(collector.get_logs()) == 1
        assert len(collector.get_metadata()) == 1

        # Clear and verify
        collector.clear()
        assert len(collector.get_orders()) == 0
        assert len(collector.get_logs()) == 0
        assert len(collector.get_metadata()) == 0

    def test_get_actions(self, collector: ActionCollector) -> None:
        """Test getting all actions as a dictionary."""
        # Add various actions
        collector.add_order("AAPL", "buy", 100)
        collector.add_log("Test log", "info")
        collector.add_metadata("key", "value")

        actions = collector.get_actions()

        assert "orders" in actions
        assert "logs" in actions
        assert "metadata" in actions

        assert len(actions["orders"]) == 1
        assert len(actions["logs"]) == 1
        assert len(actions["metadata"]) == 1

        # Check order serialization
        order_dict = actions["orders"][0]
        assert order_dict["action_type"] == ActionType.PLACE_ORDER
        assert order_dict["symbol"] == "AAPL"
        assert order_dict["side"] == "buy"
        assert order_dict["quantity"] == 100

    def test_thread_safety(self, collector: ActionCollector) -> None:
        """Test thread-safe operations."""
        import threading

        results = []

        def add_orders() -> None:
            """Add orders in a thread."""
            for i in range(100):
                order_id = collector.add_order(f"SYM{i}", "buy", i)
                results.append(order_id)

        # Create multiple threads
        threads = []
        for _ in range(5):
            thread = threading.Thread(target=add_orders)
            threads.append(thread)
            thread.start()

        # Wait for all threads
        for thread in threads:
            thread.join()

        # Check results
        orders = collector.get_orders()
        assert len(orders) == 500  # 5 threads * 100 orders
        assert len(results) == 500
        assert len(set(results)) == 500  # All order IDs should be unique

    def test_order_id_generation(self, collector: ActionCollector) -> None:
        """Test unique order ID generation."""
        order_ids = []

        # Generate multiple order IDs
        for _ in range(100):
            order_id = collector.add_order("AAPL", "buy", 100)
            order_ids.append(order_id)

        # All should be unique
        assert len(set(order_ids)) == 100

        # Check format
        for order_id in order_ids:
            assert order_id.startswith("ORD-")
            parts = order_id.split("-")
            assert len(parts) == 4  # ORD-timestamp-counter-uuid

    def test_order_action_to_dict(self) -> None:
        """Test OrderAction serialization."""
        action = OrderAction(
            action_type=ActionType.PLACE_ORDER,
            symbol="AAPL",
            side="buy",
            quantity=100,
            order_type="limit",
            price=150.0,
            order_id="ORDER-123",
            additional_params={"test": "value"},
        )

        action_dict = action.to_dict()

        assert action_dict["action_type"] == ActionType.PLACE_ORDER
        assert action_dict["symbol"] == "AAPL"
        assert action_dict["side"] == "buy"
        assert action_dict["quantity"] == 100
        assert action_dict["order_type"] == "limit"
        assert action_dict["price"] == 150.0
        assert action_dict["order_id"] == "ORDER-123"
        assert action_dict["additional_params"]["test"] == "value"
        assert "timestamp" in action_dict

    def test_log_entry_to_dict(self) -> None:
        """Test LogEntry serialization."""
        entry = LogEntry(level=LogLevel.INFO, message="Test message")

        entry_dict = entry.to_dict()

        assert entry_dict["level"] == LogLevel.INFO
        assert entry_dict["message"] == "Test message"
        assert "timestamp" in entry_dict

    def test_repr(self, collector: ActionCollector) -> None:
        """Test string representation."""
        collector.add_order("AAPL", "buy", 100)
        collector.add_log("Test", "info")
        collector.add_metadata("key", "value")

        repr_str = repr(collector)
        assert "orders=1" in repr_str
        assert "logs=1" in repr_str
        assert "metadata_keys=['key']" in repr_str
