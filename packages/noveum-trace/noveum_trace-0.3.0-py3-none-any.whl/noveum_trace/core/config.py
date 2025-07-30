"""
Configuration management for Noveum Trace SDK.

This module handles configuration loading from multiple sources including
environment variables, configuration files, and programmatic configuration.
"""

import json
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Optional, Union

import yaml

from noveum_trace.utils.exceptions import ConfigurationError

# Configuration constants
DEFAULT_ENDPOINT = "https://api.noveum.ai"
DEFAULT_TIMEOUT = 30
DEFAULT_RETRY_ATTEMPTS = 3
DEFAULT_BATCH_SIZE = 100
DEFAULT_BATCH_TIMEOUT = 5.0
DEFAULT_MAX_QUEUE_SIZE = 1000
DEFAULT_MAX_SPANS_PER_TRACE = 1000


@dataclass
class TracingConfig:
    """Configuration for tracing behavior."""

    enabled: bool = True
    sample_rate: float = 1.0
    max_spans_per_trace: int = DEFAULT_MAX_SPANS_PER_TRACE
    capture_errors: bool = True
    capture_stack_traces: bool = False
    capture_performance: bool = False


@dataclass
class TransportConfig:
    """Configuration for transport layer."""

    endpoint: str = DEFAULT_ENDPOINT
    timeout: int = DEFAULT_TIMEOUT
    retry_attempts: int = DEFAULT_RETRY_ATTEMPTS
    retry_backoff: float = 1.0
    batch_size: int = DEFAULT_BATCH_SIZE
    batch_timeout: float = DEFAULT_BATCH_TIMEOUT
    max_queue_size: int = DEFAULT_MAX_QUEUE_SIZE
    compression: bool = True


@dataclass
class SecurityConfig:
    """Configuration for security and privacy."""

    redact_pii: bool = False
    custom_redaction_patterns: list[str] = field(default_factory=list)
    encrypt_data: bool = True
    data_residency: Optional[str] = None


@dataclass
class IntegrationConfig:
    """Configuration for framework integrations."""

    langchain: dict[str, Any] = field(default_factory=lambda: {"enabled": False})
    llamaindex: dict[str, Any] = field(default_factory=lambda: {"enabled": False})
    openai: dict[str, Any] = field(default_factory=lambda: {"enabled": False})
    anthropic: dict[str, Any] = field(default_factory=lambda: {"enabled": False})


@dataclass
class Config:
    """Main configuration class for Noveum Trace SDK."""

    # Core settings
    project: Optional[str] = None
    api_key: Optional[str] = None
    environment: str = "development"

    # Component configurations
    tracing: TracingConfig = field(default_factory=TracingConfig)
    transport: TransportConfig = field(default_factory=TransportConfig)
    security: SecurityConfig = field(default_factory=SecurityConfig)
    integrations: IntegrationConfig = field(default_factory=IntegrationConfig)

    # Additional settings
    debug: bool = False
    log_level: str = "INFO"

    def __post_init__(self) -> None:
        """Validate configuration after initialization."""
        self._validate()

    def _validate(self) -> None:
        """Validate configuration values."""
        if self.tracing.sample_rate < 0 or self.tracing.sample_rate > 1:
            raise ConfigurationError(
                f"Invalid sample_rate: {self.tracing.sample_rate}. "
                "Must be between 0 and 1."
            )

        if self.tracing.max_spans_per_trace <= 0:
            raise ConfigurationError(
                f"Invalid max_spans_per_trace: {self.tracing.max_spans_per_trace}. "
                "Must be greater than 0."
            )

        if self.transport.timeout <= 0:
            raise ConfigurationError(
                f"Invalid timeout: {self.transport.timeout}. Must be greater than 0."
            )

    def to_dict(self) -> dict[str, Any]:
        """Convert configuration to dictionary."""
        return {
            "project": self.project,
            "api_key": self.api_key,
            "environment": self.environment,
            "tracing": {
                "enabled": self.tracing.enabled,
                "sample_rate": self.tracing.sample_rate,
                "max_spans_per_trace": self.tracing.max_spans_per_trace,
                "capture_errors": self.tracing.capture_errors,
                "capture_stack_traces": self.tracing.capture_stack_traces,
                "capture_performance": self.tracing.capture_performance,
            },
            "transport": {
                "endpoint": self.transport.endpoint,
                "timeout": self.transport.timeout,
                "retry_attempts": self.transport.retry_attempts,
                "retry_backoff": self.transport.retry_backoff,
                "batch_size": self.transport.batch_size,
                "batch_timeout": self.transport.batch_timeout,
                "compression": self.transport.compression,
            },
            "security": {
                "redact_pii": self.security.redact_pii,
                "custom_redaction_patterns": self.security.custom_redaction_patterns,
                "encrypt_data": self.security.encrypt_data,
                "data_residency": self.security.data_residency,
            },
            "integrations": {
                "langchain": self.integrations.langchain,
                "llamaindex": self.integrations.llamaindex,
                "openai": self.integrations.openai,
                "anthropic": self.integrations.anthropic,
            },
            "debug": self.debug,
            "log_level": self.log_level,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Config":
        """Create configuration from dictionary."""
        config = cls()

        # Core settings
        config.project = data.get("project")
        config.api_key = data.get("api_key")
        config.environment = data.get("environment", "development")
        config.debug = data.get("debug", False)
        config.log_level = data.get("log_level", "INFO")

        # Tracing configuration
        if "tracing" in data:
            tracing_data = data["tracing"]
            config.tracing = TracingConfig(
                enabled=tracing_data.get("enabled", True),
                sample_rate=tracing_data.get("sample_rate", 1.0),
                max_spans_per_trace=tracing_data.get("max_spans_per_trace", 1000),
                capture_errors=tracing_data.get("capture_errors", True),
                capture_stack_traces=tracing_data.get("capture_stack_traces", False),
                capture_performance=tracing_data.get("capture_performance", False),
            )

        # Transport configuration
        if "transport" in data:
            transport_data = data["transport"]
            config.transport = TransportConfig(
                endpoint=transport_data.get("endpoint", DEFAULT_ENDPOINT),
                timeout=transport_data.get("timeout", DEFAULT_TIMEOUT),
                retry_attempts=transport_data.get(
                    "retry_attempts", DEFAULT_RETRY_ATTEMPTS
                ),
                retry_backoff=transport_data.get("retry_backoff", 1.0),
                batch_size=transport_data.get("batch_size", DEFAULT_BATCH_SIZE),
                batch_timeout=transport_data.get(
                    "batch_timeout", DEFAULT_BATCH_TIMEOUT
                ),
                max_queue_size=transport_data.get(
                    "max_queue_size", DEFAULT_MAX_QUEUE_SIZE
                ),
                compression=transport_data.get("compression", True),
            )

        # Security configuration
        if "security" in data:
            security_data = data["security"]
            config.security = SecurityConfig(
                redact_pii=security_data.get("redact_pii", False),
                custom_redaction_patterns=security_data.get(
                    "custom_redaction_patterns", []
                ),
                encrypt_data=security_data.get("encrypt_data", True),
                data_residency=security_data.get("data_residency"),
            )

        # Integration configuration
        if "integrations" in data:
            integrations_data = data["integrations"]
            config.integrations = IntegrationConfig(
                langchain=integrations_data.get("langchain", {"enabled": False}),
                llamaindex=integrations_data.get("llamaindex", {"enabled": False}),
                openai=integrations_data.get("openai", {"enabled": False}),
                anthropic=integrations_data.get("anthropic", {"enabled": False}),
            )

        return config


# Global configuration instance
_config: Optional[Config] = None


def configure(
    config_data: Optional[Union[dict[str, Any], Config, str, Path]] = None,
) -> None:
    """
    Configure the Noveum Trace SDK.

    Args:
        config_data: Configuration data as dict, Config instance,
                    file path, or None to load from environment
    """
    global _config

    if config_data is None:
        # Load from environment and default config files
        _config = _load_from_environment()
    elif isinstance(config_data, Config):
        _config = config_data
    elif isinstance(config_data, dict):
        _config = Config.from_dict(config_data)
    elif isinstance(config_data, (str, Path)):
        _config = _load_from_file(config_data)
    else:
        raise ConfigurationError(
            f"Invalid configuration type: {type(config_data)}. "
            "Expected dict, Config, str, or Path."
        )


def get_config() -> Config:
    """
    Get the current configuration.

    Returns:
        Current Config instance

    Raises:
        ConfigurationError: If configuration has not been set
    """
    global _config
    if _config is None:
        # Auto-configure from environment
        configure()
    return _config  # type: ignore


def _load_from_environment() -> Config:
    """Load configuration from environment variables and config files."""
    config_data: dict[str, Any] = {}

    # Load from environment variables
    if os.getenv("NOVEUM_PROJECT"):
        config_data["project"] = os.getenv("NOVEUM_PROJECT")

    if os.getenv("NOVEUM_API_KEY"):
        config_data["api_key"] = os.getenv("NOVEUM_API_KEY")

    if os.getenv("NOVEUM_ENVIRONMENT"):
        config_data["environment"] = os.getenv("NOVEUM_ENVIRONMENT")

    if os.getenv("NOVEUM_ENDPOINT"):
        if "transport" not in config_data:
            config_data["transport"] = {}
        config_data["transport"]["endpoint"] = os.getenv("NOVEUM_ENDPOINT")

    debug_env = os.getenv("NOVEUM_DEBUG")
    if debug_env:
        config_data["debug"] = debug_env.lower() in ("true", "1", "yes")

    # Try to load from config files
    config_files = [
        "noveum-trace.yaml",
        "noveum-trace.yml",
        "noveum-trace.json",
        ".noveum-trace.yaml",
        ".noveum-trace.yml",
        ".noveum-trace.json",
    ]

    for config_file in config_files:
        if os.path.exists(config_file):
            file_config = _load_from_file(config_file)
            # Merge file config with environment config (env takes precedence)
            merged_config = file_config.to_dict()
            merged_config.update(config_data)
            config_data = merged_config
            break

    return Config.from_dict(config_data)


def _load_from_file(file_path: Union[str, Path]) -> Config:
    """Load configuration from a file."""
    file_path = Path(file_path)

    if not file_path.exists():
        raise ConfigurationError(f"Configuration file not found: {file_path}")

    try:
        with open(file_path) as f:
            if file_path.suffix in (".yaml", ".yml"):
                data = yaml.safe_load(f)
            elif file_path.suffix == ".json":
                data = json.load(f)
            else:
                raise ConfigurationError(
                    f"Unsupported configuration file format: {file_path.suffix}. "
                    "Supported formats: .yaml, .yml, .json"
                )

        return Config.from_dict(data or {})

    except (yaml.YAMLError, json.JSONDecodeError) as e:
        raise ConfigurationError(
            f"Failed to parse configuration file {file_path}: {e}"
        ) from e
    except Exception as e:
        raise ConfigurationError(
            f"Failed to load configuration file {file_path}: {e}"
        ) from e
