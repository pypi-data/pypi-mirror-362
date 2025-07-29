"""Command-line interface for running backtest strategies."""

import argparse
import importlib.util
import json
import logging
import sys
import traceback
from logging import Logger
from pathlib import Path
from typing import Dict, Optional, Type, cast

from tektii_sdk import Strategy, StrategyConfig
from tektii_sdk.apis import SimulatedIB, SimulatedMT4
from tektii_sdk.apis.base import SimulatedAPI
from tektii_sdk.server import serve


def load_strategy_class(module_path: str, class_name: str) -> Type[Strategy]:
    """Load a strategy class from a Python module.

    Args:
        module_path: Path to the Python module
        class_name: Name of the strategy class

    Returns:
        Strategy class

    Raises:
        FileNotFoundError: If module file doesn't exist
        ImportError: If module or class cannot be loaded
        TypeError: If class is not a Strategy subclass
    """
    # Convert to absolute path
    module_path_obj = Path(module_path).resolve()

    if not module_path_obj.exists():
        raise FileNotFoundError(f"Strategy module not found: {module_path}")

    if not module_path_obj.suffix == ".py":
        raise ValueError(f"Strategy module must be a Python file (.py): {module_path}")

    # Load module
    spec = importlib.util.spec_from_file_location("user_strategy", module_path_obj)
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot load module from {module_path}")

    module = importlib.util.module_from_spec(spec)
    sys.modules["user_strategy"] = module

    try:
        spec.loader.exec_module(module)
    except Exception as e:
        raise ImportError(f"Error loading module {module_path}: {e}")

    # Get strategy class
    if not hasattr(module, class_name):
        available_classes = [name for name in dir(module) if isinstance(getattr(module, name), type) and name != "Strategy"]
        raise ImportError(f"Class {class_name} not found in {module_path}. " f"Available classes: {', '.join(available_classes) or 'none'}")

    strategy_class = getattr(module, class_name)

    # Verify it's a Strategy subclass
    if not issubclass(strategy_class, Strategy):
        raise TypeError(f"{class_name} is not a subclass of Strategy. " f"Make sure your strategy inherits from tektii_sdk.Strategy")

    return cast(Type[Strategy], strategy_class)


def load_config(config_path: Optional[str]) -> StrategyConfig:
    """Load strategy configuration from file or create default.

    Args:
        config_path: Optional path to configuration file

    Returns:
        Strategy configuration
    """
    if config_path:
        config_path_obj = Path(config_path)
        if not config_path_obj.exists():
            raise FileNotFoundError(f"Configuration file not found: {config_path}")

        with open(config_path_obj) as f:
            if config_path_obj.suffix == ".json":
                config_data = json.load(f)
            else:
                # Assume Python file with CONFIG variable
                spec = importlib.util.spec_from_file_location("config", config_path_obj)
                if spec is None or spec.loader is None:
                    raise ImportError(f"Cannot load config from {config_path}")

                config_module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(config_module)

                if not hasattr(config_module, "CONFIG"):
                    raise ValueError(f"CONFIG variable not found in {config_path}")

                config_data = config_module.CONFIG

        return StrategyConfig(**config_data)
    else:
        # Return default configuration
        return StrategyConfig(
            name="DefaultStrategy",
            version="1.0.0",
            symbols=["BTC-USD", "ETH-USD"],
            initial_capital=10000.0,
            max_positions=5,
            risk_per_trade=0.02,
        )


def load_instrument_mapping(mapping_path: Optional[str]) -> Dict[int, str]:
    """Load instrument ID to symbol mapping.

    Args:
        mapping_path: Optional path to mapping file

    Returns:
        Instrument mapping dictionary
    """
    if mapping_path:
        mapping_path_obj = Path(mapping_path)
        if not mapping_path_obj.exists():
            raise FileNotFoundError(f"Mapping file not found: {mapping_path}")

        with open(mapping_path_obj) as f:
            mapping_data: Dict[int, str] = json.load(f)
            return mapping_data
    else:
        # Default mapping
        return {
            1: "BTC-USD",
            2: "ETH-USD",
            3: "BNB-USD",
            4: "XRP-USD",
            5: "ADA-USD",
        }


def create_api(api_type: str, strategy: Strategy) -> Optional[SimulatedAPI]:
    """Create simulated API instance.

    Args:
        api_type: Type of API to create ('ib', 'mt4', or 'none')
        strategy: Strategy instance

    Returns:
        API instance or None

    Raises:
        ValueError: If api_type is invalid
        ImportError: If requested API is not available
    """
    if api_type == "ib":
        if SimulatedIB is None:
            raise ImportError("Interactive Brokers API not available. Run 'make proto' to generate proto files.")
        return SimulatedIB(strategy.action_collector)
    elif api_type == "mt4":
        if SimulatedMT4 is None:
            raise ImportError("MT4 API not available. Run 'make proto' to generate proto files.")
        return SimulatedMT4(strategy.action_collector)
    elif api_type == "none":
        return None
    else:
        raise ValueError(f"Unknown API type: {api_type}. Valid options are: 'ib', 'mt4', 'none'")


def main() -> None:
    """Run the main command-line interface.

    Parses command-line arguments and executes the appropriate command.
    """
    # Check if we have any arguments at all
    if len(sys.argv) == 1:
        # No arguments provided, show help
        parser = create_main_parser()
        parser.print_help()
        sys.exit(1)

    # Check if first argument is a known command
    known_commands = ["run", "validate", "--help", "-h"]
    if sys.argv[1] in known_commands:
        # Use subcommand structure
        parser = create_main_parser()
        args = parser.parse_args()
    else:
        # Backwards compatibility: assume 'run' command
        # Insert 'run' at the beginning of arguments
        sys.argv.insert(1, "run")
        parser = create_main_parser()
        args = parser.parse_args()

    # Setup logging
    log_level = getattr(args, "log_level", "INFO")
    logging.basicConfig(
        level=getattr(logging, log_level),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    logger = logging.getLogger(__name__)

    # Handle commands
    if args.command == "validate":
        _handle_validate(args, logger)
    elif args.command == "run":
        _handle_run(args, logger)
    else:
        parser.print_help()
        sys.exit(1)


def create_main_parser() -> argparse.ArgumentParser:
    """Create the main argument parser with subcommands."""
    parser = argparse.ArgumentParser(
        description="Run a backtest strategy with gRPC server",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run a strategy with default settings
  tektii run my_strategy.py MyStrategy

  # Validate a strategy before uploading
  tektii validate my_strategy.py MyStrategy

  # Run with custom configuration
  tektii run my_strategy.py MyStrategy --config config.json

  # Run with IB API simulation on custom port
  tektii run my_strategy.py MyStrategy --api ib --port 50052

  # Run with instrument mapping
  tektii run my_strategy.py MyStrategy --mapping instruments.json
        """,
    )

    # Create subparsers for commands
    subparsers = parser.add_subparsers(dest="command", help="Command to run", required=True)

    # Run command
    run_parser = subparsers.add_parser("run", help="Run a strategy")
    _add_run_arguments(run_parser)

    # Validate command
    validate_parser = subparsers.add_parser("validate", help="Validate a strategy")
    _add_validate_arguments(validate_parser)

    return parser


def _add_run_arguments(parser: argparse.ArgumentParser) -> None:
    """Add arguments for run command."""
    # Required arguments
    parser.add_argument("module", help="Path to Python module containing strategy")
    parser.add_argument("class_name", help="Name of the strategy class")

    # Optional arguments
    parser.add_argument("--config", "-c", help="Path to configuration file (JSON or Python)")
    parser.add_argument(
        "--api",
        "-a",
        choices=["ib", "mt4", "none"],
        default="ib",
        help="Simulated API to use (default: ib)",
    )
    parser.add_argument("--port", "-p", type=int, default=50051, help="gRPC server port (default: 50051)")
    parser.add_argument("--mapping", "-m", help="Path to instrument ID mapping file (JSON)")
    parser.add_argument(
        "--log-level",
        "-l",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        default="INFO",
        help="Logging level (default: INFO)",
    )
    parser.add_argument(
        "--workers",
        "-w",
        type=int,
        default=10,
        help="Maximum number of worker threads (default: 10)",
    )


def _add_validate_arguments(parser: argparse.ArgumentParser) -> None:
    """Add arguments for validate command."""
    parser.add_argument("module", help="Path to Python module containing strategy")
    parser.add_argument("class_name", help="Name of the strategy class")
    parser.add_argument("--config", "-c", help="Path to configuration file to use for validation")
    parser.add_argument("--verbose", "-v", action="store_true", help="Show detailed validation output")


def _handle_validate(args: argparse.Namespace, logger: Logger) -> None:
    """Handle validate command."""
    try:
        from tektii_sdk.validator import validate_module

        logger.info(f"Validating strategy {args.class_name} from {args.module}")

        # Load config if provided
        config = None
        if args.config:
            config = load_config(args.config)

        # Run validation
        result = validate_module(args.module, args.class_name, config)

        # Print result
        print("\n" + str(result))

        # Exit with appropriate code
        sys.exit(0 if result.is_valid else 1)

    except Exception as e:
        logger.error(f"Validation failed: {e}")
        if hasattr(args, "verbose") and args.verbose:
            logger.error(traceback.format_exc())
        sys.exit(1)


def _handle_run(args: argparse.Namespace, logger: Logger) -> None:
    """Handle run command."""
    try:
        # Load strategy class
        logger.info(f"Loading strategy class {args.class_name} from {args.module}")
        strategy_class = load_strategy_class(args.module, args.class_name)

        # Load configuration
        logger.info("Loading configuration")
        config = load_config(args.config)

        # Load instrument mapping
        logger.info("Loading instrument mapping")
        instrument_mapping = load_instrument_mapping(args.mapping)

        # Create API
        logger.info(f"Creating {args.api} API")
        # Create a temporary strategy instance to get action collector
        temp_strategy = strategy_class(config)
        api = create_api(args.api, temp_strategy) if args.api != "none" else None

        # Start server
        logger.info(f"Starting gRPC server on port {args.port}")
        serve(
            strategy_class=strategy_class,
            config=config,
            api=api,
            instrument_mapping=instrument_mapping,
            port=args.port,
            max_workers=args.workers,
        )

    except Exception as e:
        logger.error(f"Failed to start strategy: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
