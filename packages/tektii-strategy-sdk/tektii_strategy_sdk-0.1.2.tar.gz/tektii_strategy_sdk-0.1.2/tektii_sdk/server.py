"""GRPC server implementation for strategy execution."""

import logging
import signal
import sys
import uuid
from concurrent import futures
from datetime import datetime
from typing import Any, Dict, Optional, Type

import grpc
from grpc_health.v1 import health, health_pb2, health_pb2_grpc

try:
    from tektii_sdk.proto import strategy_pb2, strategy_pb2_grpc
except ImportError:
    raise ImportError(
        "Proto files not available. Please run:\n"
        "  make proto\n"
        "Or manually:\n"
        "  pip install grpcio-tools\n"
        "  python -m grpc_tools.protoc -Iproto --python_out=tektii_sdk/proto"
        " --grpc_python_out=tektii_sdk/proto proto/strategy.proto"
    )


from tektii_sdk.apis.base import SimulatedAPI
from tektii_sdk.collector import ActionType
from tektii_sdk.strategy import MarketData, Position, Strategy, StrategyConfig

logger = logging.getLogger(__name__)


class StrategyServicer(strategy_pb2_grpc.StrategyServiceServicer):
    """GRPC servicer for strategy execution."""

    def __init__(
        self,
        strategy_class: Type[Strategy],
        config: StrategyConfig,
        api: Optional[SimulatedAPI] = None,
        instrument_mapping: Optional[Dict[int, str]] = None,
        health_servicer: Optional[health.HealthServicer] = None,
    ):
        """Initialize the servicer.

        Args:
            strategy_class: Strategy class to instantiate
            config: Strategy configuration
            api: Optional simulated API to use
            instrument_mapping: Optional mapping of instrument_id to symbol names
            health_servicer: Optional health servicer for updating service health
        """
        self.strategy = strategy_class(config)
        self.api = api
        self.instrument_mapping = instrument_mapping or {}
        self._initialized = False
        self._initialization_error: Optional[str] = None
        self._health_servicer = health_servicer

        # If API is provided, connect strategy to API
        if self.api:
            self.api.action_collector = self.strategy.action_collector
            self._connect_api_to_strategy()

    def _connect_api_to_strategy(self) -> None:
        """Connect the simulated API to the strategy."""
        # Register API callbacks to forward to strategy
        if self.api is not None:
            self.api.register_callback("market_data", self.strategy.emit_market_data)
            self.api.register_callback("order_update", self.strategy.on_order_update)
            self.api.register_callback("position_update", self.strategy.on_position_update)

    def _initialize_if_needed(self) -> None:
        """Initialize strategy if not already initialized."""
        if not self._initialized:
            try:
                self.strategy.initialize()

                # Connect API if available
                if self.api and not self.api.is_connected:
                    self.api.connect()

                    # Subscribe to symbols
                    if self.strategy.config.symbols:
                        self.api.subscribe_market_data(self.strategy.config.symbols)

                self._initialized = True
                self._initialization_error = None

                # Update standard health servicer if available
                if self._health_servicer:
                    self._health_servicer.set(
                        service=strategy_pb2.DESCRIPTOR.services_by_name["StrategyService"].full_name, status=health_pb2.HealthCheckResponse.SERVING
                    )
                    self._health_servicer.set("", health_pb2.HealthCheckResponse.SERVING)

            except Exception as e:
                logger.error(f"Failed to initialize strategy: {e}")
                self._initialization_error = str(e)
                raise

    def ProcessEvent(
        self, request: strategy_pb2.Event, context: grpc.ServicerContext  # type: ignore[name-defined]
    ) -> strategy_pb2.ActionResponse:  # type: ignore[name-defined]
        """Process a single event.

        Args:
            request: Event to process
            context: gRPC context

        Returns:
            Action response
        """
        try:
            # Initialize if needed
            self._initialize_if_needed()

            # Clear previous actions
            self.strategy.action_collector.clear()

            # Process event based on type
            if request.event_type == strategy_pb2.EventType.EVENT_TYPE_MARKET_DATA:  # type: ignore[attr-defined]
                self._process_candle_data(request.candle_data, request.timestamp)
            elif request.event_type == strategy_pb2.EventType.EVENT_TYPE_ORDER_EXECUTION:  # type: ignore[attr-defined]
                self._process_order_execution(request.order_execution)
            else:
                logger.warning(f"Unknown event type: {request.event_type}")
                self.strategy.action_collector.add_log(f"Unknown event type: {request.event_type}", "warning")

            # Build and return action response
            return self._build_action_response(request.event_id)

        except Exception as e:
            logger.error(f"Error processing event: {e}")
            # Add error to debug info
            self.strategy.action_collector.add_log(f"Error processing event: {str(e)}", "error")
            # Return error response with debug info
            return self._build_action_response(request.event_id)

    def _process_candle_data(self, candle_event: strategy_pb2.CandleDataEvent, timestamp: Any) -> None:  # type: ignore[name-defined]
        """Process candle data event.

        Args:
            candle_event: Candle data event
            timestamp: Event timestamp
        """
        # Map instrument_id to symbol
        instrument_id = candle_event.instrument_id
        if instrument_id not in self.instrument_mapping:
            logger.warning(f"Unknown instrument_id: {instrument_id}, using default naming")
            symbol = f"INST_{instrument_id}"
        else:
            symbol = self.instrument_mapping[instrument_id]

        # Skip if strategy doesn't track this symbol
        if symbol not in self.strategy.config.symbols:
            logger.debug(f"Ignoring data for untracked symbol: {symbol}")
            return

        # Convert timestamp
        candle_time = datetime.fromtimestamp(candle_event.candle.timestamp.seconds + candle_event.candle.timestamp.nanos / 1e9)

        # Create MarketData object
        data = MarketData(
            symbol=symbol,
            timestamp=candle_time,
            bid=float(candle_event.candle.close),  # Using close as bid for simplicity
            ask=float(candle_event.candle.close),  # Using close as ask for simplicity
            last=float(candle_event.candle.close),
            volume=candle_event.candle.volume,
            open=float(candle_event.candle.open),
            high=float(candle_event.candle.high),
            low=float(candle_event.candle.low),
            close=float(candle_event.candle.close),
        )

        # Emit to API if available, otherwise directly to strategy
        if self.api:
            self.api.emit_market_data(data)
        else:
            self.strategy.emit_market_data(data)

    def _process_order_execution(self, order_exec: strategy_pb2.OrderExecutionEvent) -> None:  # type: ignore[name-defined]
        """Process order execution event.

        Args:
            order_exec: Order execution event
        """
        # Map instrument_id to symbol
        instrument_id = order_exec.instrument_id
        if instrument_id not in self.instrument_mapping:
            logger.warning(f"Unknown instrument_id in order execution: {instrument_id}")
            symbol = f"INST_{instrument_id}"
        else:
            symbol = self.instrument_mapping[instrument_id]

        # Determine side
        side = "buy" if order_exec.direction == strategy_pb2.Direction.Direction_BUY else "sell"  # type: ignore[attr-defined]

        # Validate quantity
        if order_exec.quantity <= 0:
            logger.error(f"Invalid order quantity: {order_exec.quantity}")
            return

        # Emit order update
        if self.api:
            self.api.emit_order_update(
                order_exec.order_id,
                "filled",
                filled_quantity=order_exec.quantity,
                fill_price=order_exec.price,
            )
        else:
            self.strategy.on_order_update(order_exec.order_id, "filled", order_exec.quantity)

        # Update position
        position = self.strategy.get_position(symbol)
        if position:
            # Update existing position
            if side == "buy":
                new_quantity = position.quantity + order_exec.quantity
            else:
                new_quantity = position.quantity - order_exec.quantity

            # Calculate new average price
            if new_quantity != 0:
                if side == "buy":
                    total_value = (position.quantity * position.average_price) + (order_exec.quantity * order_exec.price)
                    new_avg_price = total_value / new_quantity
                else:
                    new_avg_price = position.average_price  # Keep same avg price when selling
            else:
                new_avg_price = 0

            updated_position = Position(
                symbol=symbol,
                quantity=new_quantity,
                average_price=new_avg_price,
                current_price=order_exec.price,
            )
        else:
            # Create new position
            quantity = order_exec.quantity if side == "buy" else -order_exec.quantity
            updated_position = Position(
                symbol=symbol,
                quantity=quantity,
                average_price=order_exec.price,
                current_price=order_exec.price,
            )

        # Emit position update
        if self.api:
            self.api.emit_position_update(updated_position)
        else:
            self.strategy.on_position_update(updated_position)

    def _build_action_response(self, event_id: str) -> strategy_pb2.ActionResponse:  # type: ignore[name-defined]
        """Build action response from collected actions.

        Args:
            event_id: Event ID to respond to

        Returns:
            Action response
        """
        response = strategy_pb2.ActionResponse(event_id=event_id, actions=[], debug_info="")  # type: ignore[attr-defined]

        # Get collected actions
        for order in self.strategy.action_collector.get_orders():
            action = strategy_pb2.Action(  # type: ignore[attr-defined]
                action_id=str(uuid.uuid4()), action_type=strategy_pb2.ActionType.ACTION_TYPE_UNSPECIFIED  # type: ignore[attr-defined]
            )

            if order.action_type == ActionType.PLACE_ORDER:
                action.action_type = strategy_pb2.ActionType.ACTION_TYPE_PLACE_ORDER  # type: ignore[attr-defined]

                # Get instrument_id from symbol (reverse mapping)
                instrument_id = 0
                for inst_id, sym in self.instrument_mapping.items():
                    if sym == order.symbol:
                        instrument_id = inst_id
                        break

                # Create place order action
                place_order = strategy_pb2.PlaceOrderAction(  # type: ignore[attr-defined]
                    instrument_id=instrument_id,
                    direction=(
                        strategy_pb2.Direction.Direction_BUY  # type: ignore[attr-defined]
                        if order.side == "buy"
                        else strategy_pb2.Direction.Direction_SELL  # type: ignore[attr-defined]
                    ),
                    quantity=int(order.quantity),
                    price=order.price or 0.0,
                )

                # Map order type
                order_type_map = {
                    "market": strategy_pb2.OrderType.ORDER_TYPE_MARKET,  # type: ignore[attr-defined]
                    "limit": strategy_pb2.OrderType.ORDER_TYPE_LIMIT,  # type: ignore[attr-defined]
                    "stop": strategy_pb2.OrderType.ORDER_TYPE_STOP,  # type: ignore[attr-defined]
                    "stop_limit": strategy_pb2.OrderType.ORDER_TYPE_STOP_LOSS,  # type: ignore[attr-defined]
                }
                place_order.order_type = order_type_map.get(order.order_type, strategy_pb2.OrderType.ORDER_TYPE_MARKET)  # type: ignore[attr-defined]

                # Set stop loss and take profit if provided
                if "sl" in order.additional_params:
                    place_order.stop_loss = float(order.additional_params["sl"])
                if "tp" in order.additional_params:
                    place_order.take_profit = float(order.additional_params["tp"])

                action.place_order.CopyFrom(place_order)

            elif order.action_type == ActionType.CANCEL_ORDER:
                action.action_type = strategy_pb2.ActionType.ACTION_TYPE_CANCEL_ORDER  # type: ignore[attr-defined]

                # Create cancel order action
                cancel_order = strategy_pb2.CancelOrderAction(order_id=order.order_id or "")  # type: ignore[attr-defined]
                action.cancel_order.CopyFrom(cancel_order)

            response.actions.append(action)

        # Add debug info from logs
        logs = self.strategy.action_collector.get_logs()
        if logs:
            debug_lines = [f"[{log.level.upper()}] {log.message}" for log in logs]
            response.debug_info = "\n".join(debug_lines)

        return response


def serve(
    strategy_class: Type[Strategy],
    config: StrategyConfig,
    api: Optional[SimulatedAPI] = None,
    instrument_mapping: Optional[Dict[int, str]] = None,
    port: int = 50051,
    max_workers: int = 10,
    health_servicer: Optional[health.HealthServicer] = None,
) -> None:
    """Start the gRPC server.

    Args:
        strategy_class: Strategy class to serve
        config: Strategy configuration
        api: Optional simulated API to use
        instrument_mapping: Optional mapping of instrument_id to symbol names
        port: Port to listen on
        max_workers: Maximum number of worker threads
        health_servicer: Optional health servicer to use (creates one if not provided)
    """
    # Setup logging
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    # Create server
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=max_workers))

    # Add servicer
    servicer = StrategyServicer(strategy_class, config, api, instrument_mapping, health_servicer)
    strategy_pb2_grpc.add_StrategyServiceServicer_to_server(servicer, server)

    # Add standard gRPC health servicer
    if health_servicer is None:
        health_servicer = health.HealthServicer()
    health_pb2_grpc.add_HealthServicer_to_server(health_servicer, server)

    # Set the initial health status for the service
    health_servicer.set(
        service=strategy_pb2.DESCRIPTOR.services_by_name["StrategyService"].full_name, status=health_pb2.HealthCheckResponse.NOT_SERVING
    )
    # Also set overall server health
    health_servicer.set("", health_pb2.HealthCheckResponse.NOT_SERVING)

    # Enable reflection for debugging
    try:
        from grpc_reflection.v1alpha import reflection

        SERVICE_NAMES = (
            strategy_pb2.DESCRIPTOR.services_by_name["StrategyService"].full_name,
            reflection.SERVICE_NAME,
        )
        reflection.enable_server_reflection(SERVICE_NAMES, server)
        logger.info("gRPC reflection enabled")
    except ImportError:
        logger.warning("grpc_reflection not available - install with: pip install grpcio-reflection")

    # Listen on port
    server.add_insecure_port(f"[::]:{port}")

    # Setup signal handlers for graceful shutdown
    def signal_handler(sig: int, frame: Any) -> None:
        logger.info("Shutting down server...")
        # Update health status to NOT_SERVING during shutdown
        health_servicer.set(
            service=strategy_pb2.DESCRIPTOR.services_by_name["StrategyService"].full_name, status=health_pb2.HealthCheckResponse.NOT_SERVING
        )
        health_servicer.set("", health_pb2.HealthCheckResponse.NOT_SERVING)

        servicer.strategy.shutdown()
        if servicer.api and servicer.api.is_connected:
            servicer.api.disconnect()
        server.stop(grace=5)
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    # Start server
    server.start()
    logger.info(f"Strategy server started on port {port}")
    logger.info(f"Serving strategy: {config.name} v{config.version}")

    # Now that server has started, update health status to SERVING
    health_servicer.set(service=strategy_pb2.DESCRIPTOR.services_by_name["StrategyService"].full_name, status=health_pb2.HealthCheckResponse.SERVING)
    health_servicer.set("", health_pb2.HealthCheckResponse.SERVING)

    # Wait for termination
    server.wait_for_termination()
