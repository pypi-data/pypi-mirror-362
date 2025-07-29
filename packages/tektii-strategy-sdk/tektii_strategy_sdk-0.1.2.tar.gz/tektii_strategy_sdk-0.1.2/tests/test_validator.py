"""Tests for the strategy validator."""

from tektii_sdk import Strategy, StrategyConfig
from tektii_sdk.strategy import MarketData
from tektii_sdk.validator import ValidationResult, validate_strategy


class ValidTestStrategy(Strategy):
    """A valid test strategy."""

    def on_start(self) -> None:
        """Initialize the strategy."""
        self.started = True

    def on_market_data(self, data: MarketData) -> None:
        """Process market data."""
        if data.last > 100:
            self.buy(data.symbol, 10)


class InvalidInheritanceStrategy:
    """Doesn't inherit from Strategy."""

    def on_market_data(self, data: MarketData) -> None:
        """Process market data."""


class MissingMethodStrategy(Strategy):
    """Missing required on_market_data method."""

    def on_start(self) -> None:
        """Initialize the strategy."""


class ErrorProneStrategy(Strategy):
    """Strategy that throws errors."""

    def on_start(self) -> None:
        """Initialize the strategy."""
        raise ValueError("Startup error")

    def on_market_data(self, data: MarketData) -> None:
        """Process market data."""
        raise RuntimeError("Processing error")


class SlowStrategy(Strategy):
    """Strategy that's slow to process."""

    def on_start(self) -> None:
        """Initialize the strategy."""

    def on_market_data(self, data: MarketData) -> None:
        """Process market data."""
        import time

        time.sleep(0.01)  # Simulate slow processing


class TestStrategyValidator:
    """Test cases for StrategyValidator."""

    def test_valid_strategy(self) -> None:
        """Test validation of a valid strategy."""
        result = validate_strategy(ValidTestStrategy)

        assert result.is_valid
        assert len(result.errors) == 0
        assert "inheritance" in result.info
        assert "✓" in result.info["inheritance"]

    def test_invalid_inheritance(self) -> None:
        """Test validation of strategy with wrong inheritance."""
        result = validate_strategy(InvalidInheritanceStrategy)  # type: ignore[arg-type]

        assert not result.is_valid
        assert len(result.errors) > 0
        assert any("does not inherit from" in error for error in result.errors)

    def test_missing_method(self) -> None:
        """Test validation of strategy missing required method."""
        result = validate_strategy(MissingMethodStrategy)  # type: ignore[type-abstract]

        assert not result.is_valid
        assert any("not implemented" in error for error in result.errors)

    def test_error_prone_strategy(self) -> None:
        """Test validation of strategy that throws errors."""
        result = validate_strategy(ErrorProneStrategy)

        assert not result.is_valid
        assert any("Failed to initialize" in error for error in result.errors)

    def test_performance_warning(self) -> None:
        """Test performance validation."""
        result = validate_strategy(SlowStrategy)

        # Should be valid but with warnings
        assert result.is_valid
        assert len(result.warnings) > 0
        assert any("too slow" in warning for warning in result.warnings)

    def test_custom_config(self) -> None:
        """Test validation with custom configuration."""
        config = StrategyConfig(name="CustomTest", version="2.0.0", symbols=["TEST1"], parameters={"threshold": 200})

        result = validate_strategy(ValidTestStrategy, config)

        assert result.is_valid
        assert result.info["strategy_name"] == "CustomTest"
        assert result.info["strategy_version"] == "2.0.0"

    def test_validation_result_string(self) -> None:
        """Test ValidationResult string representation."""
        result = ValidationResult(is_valid=True, errors=[], warnings=[], info={})
        result.add_warning("Test warning")
        result.info["test"] = "value"

        result_str = str(result)
        assert "✅" in result_str
        assert "Test warning" in result_str
        assert "test: value" in result_str

    def test_validation_result_error(self) -> None:
        """Test ValidationResult with errors."""
        result = ValidationResult(is_valid=True, errors=[], warnings=[], info={})
        result.add_error("Test error")

        assert not result.is_valid
        assert "Test error" in result.errors
        assert "❌" in str(result)

    def test_order_validation_check(self) -> None:
        """Test order validation checking."""

        class NoValidationStrategy(Strategy):
            def on_start(self) -> None:
                pass

            def on_market_data(self, data: MarketData) -> None:
                # This strategy doesn't validate orders
                self._place_order = lambda x: "fake_id"  # type: ignore[assignment]

        result = validate_strategy(NoValidationStrategy)

        # Should have a warning about order validation
        assert any("validate" in warning for warning in result.warnings)

    def test_large_data_structure_warning(self) -> None:
        """Test warning for large data structures."""

        class LargeDataStrategy(Strategy):
            def __init__(self, config: StrategyConfig):
                super().__init__(config)
                self.huge_list = list(range(10000))

            def on_start(self) -> None:
                pass

            def on_market_data(self, data: MarketData) -> None:
                pass

        result = validate_strategy(LargeDataStrategy)

        assert len(result.warnings) > 0
        assert any("Large data structure" in warning for warning in result.warnings)
