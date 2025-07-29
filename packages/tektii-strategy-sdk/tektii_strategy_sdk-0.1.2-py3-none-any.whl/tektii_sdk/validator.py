"""Strategy validation module for pre-upload checks."""

import logging
import traceback
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, List, Optional, Type

from tektii_sdk import Strategy, StrategyConfig
from tektii_sdk.exceptions import ValidationError
from tektii_sdk.strategy import MarketData, TimeFrame

logger = logging.getLogger(__name__)


@dataclass
class ValidationResult:
    """Result of strategy validation."""

    is_valid: bool
    errors: List[str]
    warnings: List[str]
    info: Dict[str, Any]

    def add_error(self, message: str) -> None:
        """Add an error message."""
        self.errors.append(message)
        self.is_valid = False

    def add_warning(self, message: str) -> None:
        """Add a warning message."""
        self.warnings.append(message)

    def __str__(self) -> str:
        """Return string representation of the validation result."""
        lines = []

        if self.is_valid:
            lines.append("✅ Strategy validation PASSED")
        else:
            lines.append("❌ Strategy validation FAILED")

        if self.errors:
            lines.append("\nErrors:")
            for error in self.errors:
                lines.append(f"  ❌ {error}")

        if self.warnings:
            lines.append("\nWarnings:")
            for warning in self.warnings:
                lines.append(f"  ⚠️  {warning}")

        if self.info:
            lines.append("\nInfo:")
            for key, value in self.info.items():
                lines.append(f"  • {key}: {value}")

        return "\n".join(lines)


class StrategyValidator:
    """Validator for trading strategies."""

    def __init__(self, strategy_class: Type[Strategy], config: Optional[StrategyConfig] = None) -> None:
        """Initialize validator.

        Args:
            strategy_class: Strategy class to validate
            config: Optional configuration to use for testing
        """
        self.strategy_class = strategy_class
        self.config = config or self._create_default_config()
        self.result = ValidationResult(is_valid=True, errors=[], warnings=[], info={})

    def _create_default_config(self) -> StrategyConfig:
        """Create a default configuration for testing."""
        return StrategyConfig(
            name="ValidationTest",
            version="1.0.0",
            symbols=["TEST1", "TEST2"],
            timeframes=[TimeFrame.M5],
            initial_capital=10000.0,
            max_positions=2,
            parameters={},
            risk_per_trade=0.01,
        )

    def validate(self) -> ValidationResult:
        """Run all validation checks.

        Returns:
            Validation result
        """
        # Check inheritance
        self._check_inheritance()

        # Check required methods
        self._check_required_methods()

        # Check instantiation
        strategy_instance = self._check_instantiation()

        if strategy_instance:
            # Check initialization
            self._check_initialization(strategy_instance)

            # Check market data handling
            self._check_market_data_handling(strategy_instance)

            # Check order placement
            self._check_order_placement(strategy_instance)

            # Check error handling
            self._check_error_handling(strategy_instance)

            # Check performance
            self._check_performance(strategy_instance)

            # Collect strategy info
            self._collect_strategy_info(strategy_instance)

        return self.result

    def _check_inheritance(self) -> None:
        """Check that the class inherits from Strategy."""
        if not issubclass(self.strategy_class, Strategy):
            self.result.add_error(f"{self.strategy_class.__name__} does not inherit from tektii_sdk.Strategy")  # type: ignore[unreachable]
        else:
            self.result.info["inheritance"] = "✓ Correctly inherits from Strategy"

    def _check_required_methods(self) -> None:
        """Check that required methods are implemented."""
        required_methods = ["on_start", "on_market_data"]

        for method_name in required_methods:
            if not hasattr(self.strategy_class, method_name):
                self.result.add_error(f"Missing required method: {method_name}")
            else:
                method = getattr(self.strategy_class, method_name)
                if not callable(method):
                    self.result.add_error(f"{method_name} is not callable")
                else:
                    # Check if it's actually implemented (not just inherited abstract)
                    if method.__qualname__ == f"Strategy.{method_name}":
                        self.result.add_error(f"{method_name} is not implemented (using base class method)")

        # Check optional methods
        optional_methods = ["on_stop", "on_order_update", "on_position_update"]
        implemented_optional = []

        for method_name in optional_methods:
            if hasattr(self.strategy_class, method_name):
                method = getattr(self.strategy_class, method_name)
                if method.__qualname__ != f"Strategy.{method_name}":
                    implemented_optional.append(method_name)

        if implemented_optional:
            self.result.info["optional_methods"] = f"Implements: {', '.join(implemented_optional)}"

    def _check_instantiation(self) -> Optional[Strategy]:
        """Check that the strategy can be instantiated."""
        try:
            strategy = self.strategy_class(self.config)
            self.result.info["instantiation"] = "✓ Successfully instantiated"
            return strategy
        except Exception as e:
            self.result.add_error(f"Failed to instantiate strategy: {str(e)}")
            self.result.info["instantiation_traceback"] = traceback.format_exc()
            return None

    def _check_initialization(self, strategy: Strategy) -> None:
        """Check that the strategy can be initialized."""
        try:
            strategy.initialize()
            self.result.info["initialization"] = "✓ Successfully initialized"

            # Check if on_start was called
            if hasattr(strategy, "_initialized") and strategy._initialized:
                self.result.info["on_start_called"] = "✓ on_start was called"

        except Exception as e:
            self.result.add_error(f"Failed to initialize strategy: {str(e)}")
            self.result.info["initialization_traceback"] = traceback.format_exc()

    def _check_market_data_handling(self, strategy: Strategy) -> None:
        """Check market data processing."""
        try:
            # Create sample market data
            test_data = MarketData(
                symbol="TEST1",
                timestamp=datetime.now(),
                bid=100.0,
                ask=100.1,
                last=100.05,
                volume=1000000,
                open=99.0,
                high=101.0,
                low=98.5,
                close=100.05,
            )

            # Process market data
            strategy.emit_market_data(test_data)

            self.result.info["market_data_handling"] = "✓ Processes market data without errors"

            # Check if any actions were taken
            actions = strategy.action_collector.get_actions()
            if actions["orders"]:
                self.result.info["places_orders"] = f"✓ Places orders ({len(actions['orders'])} found)"

            # Check if _place_order has been overridden after market data processing
            if hasattr(strategy, "_place_order"):
                place_order_method = strategy._place_order

                # Get the original _place_order method from the Strategy base class
                original_place_order = None
                for base_class in strategy.__class__.__mro__:
                    if base_class.__name__ == "Strategy" and hasattr(base_class, "_place_order"):
                        original_place_order = base_class._place_order
                        break

                # Check if the method has been replaced
                is_overridden = False
                warning_msg = None

                # Check if it's a lambda function
                if hasattr(place_order_method, "__name__") and place_order_method.__name__ == "<lambda>":
                    is_overridden = True
                    warning_msg = "" "Strategy overrides _place_order with a lambda function, " "which may bypass order validate checks"
                # Check if it's not a method (e.g., assigned function)
                elif not hasattr(place_order_method, "__self__"):
                    is_overridden = True
                    warning_msg = "Strategy replaces _place_order with a function that may bypass validation"
                # Check if it's different from the original
                elif original_place_order and place_order_method != original_place_order:
                    # Additional check: see if it's been reassigned at runtime
                    try:
                        # Get the method from the instance's class
                        class_method = getattr(strategy.__class__, "_place_order", None)
                        if class_method != place_order_method:
                            is_overridden = True
                            warning_msg = "Strategy modifies _place_order at runtime, " "which may bypass validate checks"
                    except Exception:
                        pass

                if is_overridden and warning_msg:
                    self.result.add_warning(warning_msg)

        except Exception as e:
            self.result.add_error(f"Error processing market data: {str(e)}")
            self.result.info["market_data_traceback"] = traceback.format_exc()

    def _check_order_placement(self, strategy: Strategy) -> None:
        """Check order placement capabilities."""
        try:
            # Clear any previous actions
            strategy.action_collector.clear()

            # Test buy order
            order_id = strategy.buy("TEST1", 10, "market")
            if order_id:
                self.result.info["buy_orders"] = "✓ Can place buy orders"

            # Test sell order
            order_id = strategy.sell("TEST1", 10, "limit", price=100.0)
            if order_id:
                self.result.info["sell_orders"] = "✓ Can place sell orders"

            # Check order validation
            try:
                strategy.buy("TEST1", -10, "market")  # Invalid quantity
                self.result.add_warning("Strategy does not validate negative quantities")
            except (ValueError, ValidationError):
                self.result.info["order_validation"] = "✓ Validates order parameters"

        except Exception as e:
            self.result.add_warning(f"Issue with order placement: {str(e)}")

    def _check_error_handling(self, strategy: Strategy) -> None:
        """Check error handling capabilities."""
        # Test with invalid data
        try:
            invalid_data = MarketData(
                symbol="INVALID",
                timestamp=datetime.now(),
                bid=-100.0,  # Invalid negative price
                ask=-99.0,
                last=-99.5,
                volume=-1000,
            )

            strategy.emit_market_data(invalid_data)

            # Check if errors were logged
            logs = strategy.action_collector.get_logs()
            error_logs = [log for log in logs if log.level.value == "error"]

            if error_logs:
                self.result.info["error_handling"] = "✓ Logs errors appropriately"
            else:
                self.result.add_warning("Strategy may not handle invalid data properly (no error logs found)")

        except Exception:
            # This is actually good - strategy rejected invalid data
            self.result.info["data_validation"] = "✓ Rejects invalid market data"

    def _check_performance(self, strategy: Strategy) -> None:
        """Check performance characteristics."""
        import time

        # Measure market data processing time
        test_data = MarketData(
            symbol="TEST1",
            timestamp=datetime.now(),
            bid=100.0,
            ask=100.1,
            last=100.05,
            volume=1000000,
        )

        # Process multiple events
        num_events = 1000
        start_time = time.time()

        for _ in range(num_events):
            strategy.emit_market_data(test_data)

        elapsed_time = time.time() - start_time
        events_per_second = num_events / elapsed_time

        self.result.info["performance"] = f"Processes {events_per_second:.0f} events/second"

        if events_per_second < 100:
            self.result.add_warning(
                f"Strategy may be too slow for high-frequency \
                    trading ({events_per_second:.0f} events/sec)"
            )

    def _collect_strategy_info(self, strategy: Strategy) -> None:
        """Collect information about the strategy."""
        # Get docstring
        if strategy.__class__.__doc__:
            self.result.info["description"] = strategy.__class__.__doc__.strip().split("\n")[0]

        # Get config info
        self.result.info["strategy_name"] = strategy.config.name
        self.result.info["strategy_version"] = strategy.config.version
        self.result.info["symbols"] = ", ".join(strategy.config.symbols)
        self.result.info["max_positions"] = strategy.config.max_positions

        # Check for custom parameters
        if strategy.config.parameters:
            self.result.info["parameters"] = ", ".join(f"{k}={v}" for k, v in strategy.config.parameters.items())

        # Check memory usage
        import sys

        size = sys.getsizeof(strategy)
        self.result.info["memory_usage"] = f"{size} bytes"

        # Check for large data structures
        for attr_name in dir(strategy):
            if not attr_name.startswith("_"):
                attr = getattr(strategy, attr_name)
                if hasattr(attr, "__len__"):
                    try:
                        length = len(attr)
                        if length > 1000:
                            self.result.add_warning(f"Large data structure found: {attr_name} has {length} items")
                    except Exception:
                        pass


def validate_strategy(strategy_class: Type[Strategy], config: Optional[StrategyConfig] = None) -> ValidationResult:
    """Validate a strategy class.

    Args:
        strategy_class: Strategy class to validate
        config: Optional configuration to use for testing

    Returns:
        Validation result
    """
    validator = StrategyValidator(strategy_class, config)
    return validator.validate()


def validate_module(module_path: str, class_name: str, config: Optional[StrategyConfig] = None) -> ValidationResult:
    """Validate a strategy from a module file.

    Args:
        module_path: Path to Python module
        class_name: Name of strategy class
        config: Optional configuration to use for testing

    Returns:
        Validation result
    """
    from tektii_sdk.cli import load_strategy_class

    try:
        strategy_class = load_strategy_class(module_path, class_name)
        return validate_strategy(strategy_class, config)
    except Exception as e:
        result = ValidationResult(is_valid=False, errors=[], warnings=[], info={})
        result.add_error(f"Failed to load strategy: {str(e)}")
        return result
