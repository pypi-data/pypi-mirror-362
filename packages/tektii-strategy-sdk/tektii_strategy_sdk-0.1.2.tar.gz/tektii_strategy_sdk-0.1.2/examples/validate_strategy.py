#!/usr/bin/env python3
"""Example of validating strategies before deployment.

This script shows how to validate your strategies to ensure they're
compatible with the backtesting platform before uploading.
"""

from typing import Any, List

from tektii_sdk import Strategy, StrategyConfig
from tektii_sdk.strategy import MarketData
from tektii_sdk.validator import validate_module, validate_strategy


# Example 1: A valid strategy
class ValidStrategy(Strategy):
    """A properly implemented strategy."""

    def __init__(self, config: StrategyConfig):
        """Initialize the strategy with configuration."""
        super().__init__(config)
        self.threshold = config.parameters.get("threshold", 100.0)
        self.position_size = config.parameters.get("position_size", 10)

    def on_start(self) -> None:
        """Initialize strategy."""
        self.log("Valid strategy started")
        self.position_count = 0

    def on_market_data(self, data: MarketData) -> None:
        """Process market data."""
        if data.last < self.threshold and self.position_count == 0:
            self.buy(data.symbol, self.position_size)
            self.position_count += 1
        elif data.last > self.threshold * 1.1 and self.position_count > 0:
            self.sell(data.symbol, self.position_size)
            self.position_count -= 1

    def on_stop(self) -> None:
        """Cleanup on stop."""
        self.log("Valid strategy stopped")


# Example 2: A strategy with issues
class ProblematicStrategy(Strategy):
    """A strategy with some problems."""

    def __init__(self, config: StrategyConfig):
        """Initialize the strategy with configuration."""
        super().__init__(config)
        # Creating a large data structure (warning)
        self.price_history = [0] * 100000

    def on_start(self) -> None:
        """Initialize strategy."""
        # Missing implementation details

    def on_market_data(self, data: MarketData) -> None:
        """Process market data - has performance issues."""
        # Inefficient implementation
        import time

        time.sleep(0.01)  # Simulating slow processing

        # Not validating data
        self.buy(data.symbol, -10)  # Negative quantity!


# Example 3: An invalid strategy
class InvalidStrategy:
    """This doesn't inherit from Strategy - will fail validation."""

    def on_market_data(self, data: Any) -> None:
        """Process market data."""
        print("This won't work!")


def validate_examples() -> None:
    """Run validation on example strategies."""
    print("Strategy Validation Examples")
    print("=" * 50)

    # Example 1: Validate a good strategy
    print("\n1. Validating ValidStrategy:")
    print("-" * 30)

    config = StrategyConfig(
        name="ValidExample",
        version="1.0.0",
        symbols=["BTC-USD", "ETH-USD"],
        parameters={"threshold": 50000.0, "position_size": 0.1},
    )

    result = validate_strategy(ValidStrategy, config)
    print(result)

    # Example 2: Validate a problematic strategy
    print("\n2. Validating ProblematicStrategy:")
    print("-" * 30)

    result = validate_strategy(ProblematicStrategy, config)
    print(result)

    # Example 3: Validate an invalid strategy
    print("\n3. Validating InvalidStrategy:")
    print("-" * 30)

    result = validate_strategy(InvalidStrategy, config)  # type: ignore[arg-type]
    print(result)

    # Example 4: Validate from file
    print("\n4. Validating from file (simple_ma_strategy.py):")
    print("-" * 30)

    try:
        result = validate_module("simple_ma_strategy.py", "SimpleMAStrategy", config)
        print(result)
    except Exception as e:
        print(f"Error: {e}")


def validate_custom_strategy() -> None:
    """Validate a custom strategy with specific requirements."""
    print("\n\nCustom Validation Example")
    print("=" * 50)

    class CustomStrategy(Strategy):
        """Strategy with custom validation requirements."""

        def __init__(self, config: StrategyConfig):
            super().__init__(config)
            # Check for required parameters
            if "ma_period" not in config.parameters:
                raise ValueError("ma_period parameter is required")

            self.ma_period = config.parameters["ma_period"]
            self.prices: List[float] = []

        def on_start(self) -> None:
            self.log(f"Starting with MA period: {self.ma_period}")

        def on_market_data(self, data: MarketData) -> None:
            self.prices.append(data.last)
            if len(self.prices) > self.ma_period:
                self.prices.pop(0)

            if len(self.prices) == self.ma_period:
                ma = sum(self.prices) / self.ma_period
                if data.last > ma:
                    self.buy(data.symbol, 1)

    # Test with missing parameter
    print("\nTesting with missing required parameter:")
    config_missing = StrategyConfig(name="Test", version="1.0.0")
    result = validate_strategy(CustomStrategy, config_missing)
    print(result)

    # Test with correct parameter
    print("\nTesting with correct parameter:")
    config_correct = StrategyConfig(name="Test", version="1.0.0", parameters={"ma_period": 20})
    result = validate_strategy(CustomStrategy, config_correct)
    print(result)


def main() -> None:
    """Run all validation examples."""
    validate_examples()
    validate_custom_strategy()

    print("\n\nValidation Tips:")
    print("=" * 50)
    print("1. Always validate your strategy before uploading")
    print("2. Fix all errors before deployment")
    print("3. Consider warnings for production use")
    print("4. Use 'tektii validate' command for quick checks")
    print("\nExample command:")
    print("  tektii validate my_strategy.py MyStrategy")


if __name__ == "__main__":
    main()
