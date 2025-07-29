# Backtest Strategy SDK Examples

This directory contains example strategies and configurations to help you get started with the Backtest Strategy SDK.

## Files

- `simple_ma_strategy.py` - A basic moving average crossover strategy
- `rsi_strategy.py` - An RSI mean reversion strategy with risk management
- `validate_strategy.py` - Examples of strategy validation
- `ma_config.json` - Configuration file for the MA strategy
- `instruments.json` - Instrument ID to symbol mapping

## Running Examples

### 1. Validate a Strategy

Always validate your strategy before deployment:

```bash
# Validate a strategy
tektii validate simple_ma_strategy.py SimpleMAStrategy

# Validate with custom config
tektii validate simple_ma_strategy.py SimpleMAStrategy --config ma_config.json

# Run validation examples
python validate_strategy.py
```

### 2. Direct Python Execution

Run a strategy directly:

```bash
python simple_ma_strategy.py
```

### 3. Using the CLI

Run with the command-line interface:

```bash
# Basic usage
tektii run simple_ma_strategy.py SimpleMAStrategy

# With configuration file
tektii run simple_ma_strategy.py SimpleMAStrategy --config ma_config.json

# With custom port and API
tektii run simple_ma_strategy.py SimpleMAStrategy --port 50052 --api ib

# With instrument mapping
tektii run simple_ma_strategy.py SimpleMAStrategy --mapping instruments.json
```

## Creating Your Own Strategy

1. **Copy the template**:
   ```bash
   cp simple_ma_strategy.py my_strategy.py
   ```

2. **Modify the strategy logic**:
   - Update the `on_market_data` method with your logic
   - Add any indicators or state tracking in `on_start`
   - Implement position management

3. **Create a configuration**:
   ```json
   {
     "name": "MyStrategy",
     "version": "1.0.0",
     "symbols": ["BTC-USD", "ETH-USD"],
     "parameters": {
       "my_param": 42
     }
   }
   ```

4. **Run your strategy**:
   ```bash
   tektii my_strategy.py MyStrategy --config my_config.json
   ```

## Testing with grpcurl

You can test your running strategy using grpcurl:

```bash
# Check health
grpcurl -plaintext localhost:50051 backtest.v1.StrategyService/HealthCheck

# Send a test event (requires event.json file)
grpcurl -plaintext -d @ localhost:50051 backtest.v1.StrategyService/ProcessEvent < event.json
```

Example `event.json`:
```json
{
  "event_id": "test-001",
  "timestamp": "2024-01-01T00:00:00Z",
  "event_type": "EVENT_TYPE_MARKET_DATA",
  "candle_data": {
    "instrument_id": 1,
    "timeframe_id": 5,
    "exchange": "BINANCE",
    "candle": {
      "timestamp": "2024-01-01T00:00:00Z",
      "open": "42000.0",
      "high": "42500.0",
      "low": "41500.0",
      "close": "42200.0",
      "volume": 1000
    }
  }
}
```

## Strategy Best Practices

1. **State Management**: Initialize all state in `on_start()`
2. **Error Handling**: Always wrap risky operations in try-except blocks
3. **Logging**: Use `self.log()` for important events
4. **Position Sizing**: Implement proper risk management
5. **Performance**: Avoid heavy computations in `on_market_data()`

## Debugging

Enable debug logging:
```bash
tektii my_strategy.py MyStrategy --log-level DEBUG
```

Common issues:
- **Port already in use**: Change port with `--port`
- **Module not found**: Ensure the strategy file is in the Python path
- **Invalid configuration**: Check JSON syntax and required fields
- **No market data**: Verify instrument mapping matches your symbols
