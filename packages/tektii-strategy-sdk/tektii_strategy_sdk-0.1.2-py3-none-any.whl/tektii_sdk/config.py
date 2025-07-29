"""Configuration management for the backtest SDK."""

from typing import Any, Dict, Optional

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class ServerConfig(BaseSettings):
    """GRPC server configuration."""

    model_config = SettingsConfigDict(
        env_prefix="BACKTEST_",
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    # Server settings
    grpc_port: int = Field(default=50051, description="gRPC server port")
    grpc_max_workers: int = Field(default=10, description="Maximum worker threads for gRPC server")
    grpc_max_message_size: int = Field(default=4 * 1024 * 1024, description="Maximum message size in bytes")  # 4MB
    grpc_keepalive_time_ms: int = Field(default=10000, description="How often to ping clients to keep connection alive (ms)")

    # Logging settings
    log_level: str = Field(default="INFO", description="Logging level")
    log_format: str = Field(default="%(asctime)s - %(name)s - %(levelname)s - %(message)s", description="Log format string")
    log_file: Optional[str] = Field(default=None, description="Log file path (None for stdout)")

    # Security settings
    enable_tls: bool = Field(default=False, description="Enable TLS for gRPC")
    tls_cert_file: Optional[str] = Field(default=None, description="TLS certificate file path")
    tls_key_file: Optional[str] = Field(default=None, description="TLS key file path")

    # Performance settings
    enable_reflection: bool = Field(default=True, description="Enable gRPC reflection for debugging")
    enable_compression: bool = Field(default=True, description="Enable gRPC compression")

    def validate_log_level(cls, v: str) -> str:
        """Validate log level."""
        valid_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        v = v.upper()
        if v not in valid_levels:
            raise ValueError(f"Invalid log level: {v}. Must be one of {valid_levels}")
        return v


class BacktestConfig(BaseSettings):
    """Backtest-specific configuration."""

    model_config = SettingsConfigDict(
        env_prefix="BACKTEST_",
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    # Simulation settings
    initial_balance: float = Field(default=100000.0, description="Initial account balance")
    commission_rate: float = Field(default=0.001, description="Commission rate (0.1%)")
    slippage_rate: float = Field(default=0.0001, description="Slippage rate (0.01%)")

    # Risk management
    max_position_size: float = Field(default=0.1, description="Max position size as fraction of capital")
    max_leverage: float = Field(default=1.0, description="Maximum leverage allowed")
    stop_loss_pct: Optional[float] = Field(default=None, description="Default stop loss percentage")

    # Data settings
    warmup_periods: int = Field(default=0, description="Number of periods for indicator warmup")

    # Execution settings
    fill_at_last: bool = Field(default=True, description="Fill orders at last price (vs bid/ask)")
    partial_fills: bool = Field(default=False, description="Allow partial order fills")


class DockerConfig(BaseSettings):
    """Docker container configuration."""

    model_config = SettingsConfigDict(
        env_prefix="DOCKER_",
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    # Resource limits
    memory_limit: str = Field(default="512m", description="Container memory limit")
    cpu_limit: float = Field(default=1.0, description="Container CPU limit (cores)")

    # Security
    read_only_root: bool = Field(default=True, description="Make root filesystem read-only")
    no_new_privileges: bool = Field(default=True, description="Prevent privilege escalation")
    user: str = Field(default="strategy:strategy", description="User to run as (user:group)")

    # Networking
    network_mode: str = Field(default="bridge", description="Docker network mode")

    # Volumes
    data_volume: Optional[str] = Field(default=None, description="Data volume mount path")
    log_volume: Optional[str] = Field(default=None, description="Log volume mount path")


class Config:
    """Main configuration container."""

    def __init__(self) -> None:
        """Initialize configuration."""
        self.server = ServerConfig()
        self.backtest = BacktestConfig()
        self.docker = DockerConfig()

    @classmethod
    def from_env(cls) -> "Config":
        """Create configuration from environment variables."""
        return cls()

    @classmethod
    def from_dict(cls, config_dict: Dict[str, Any]) -> "Config":
        """Create configuration from dictionary.

        Args:
            config_dict: Configuration dictionary

        Returns:
            Config instance
        """
        config = cls()

        # Update server config
        if "server" in config_dict:
            config.server = ServerConfig(**config_dict["server"])

        # Update backtest config
        if "backtest" in config_dict:
            config.backtest = BacktestConfig(**config_dict["backtest"])

        # Update docker config
        if "docker" in config_dict:
            config.docker = DockerConfig(**config_dict["docker"])

        return config

    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary.

        Returns:
            Configuration dictionary
        """
        return {
            "server": self.server.model_dump(),
            "backtest": self.backtest.model_dump(),
            "docker": self.docker.model_dump(),
        }


# Global configuration instance
_config: Optional[Config] = None


def get_config() -> Config:
    """Get global configuration instance.

    Returns:
        Configuration instance
    """
    global _config
    if _config is None:
        _config = Config.from_env()
    return _config


def set_config(config: Config) -> None:
    """Set global configuration instance.

    Args:
        config: Configuration instance
    """
    global _config
    _config = config
