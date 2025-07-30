"""
Utility functions and classes for Upstream SDK.
"""

import json
import logging
import os
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional, Union

import yaml

from .exceptions import ConfigurationError

logger = logging.getLogger(__name__)


class ConfigManager:
    """
    Configuration manager for Upstream SDK.
    """

    def __init__(
        self,
        username: Optional[str] = None,
        password: Optional[str] = None,
        base_url: Optional[str] = None,
        ckan_url: Optional[str] = None,
        timeout: int = 30,
        max_retries: int = 3,
        chunk_size: int = 10000,
        max_chunk_size_mb: int = 50,
        **kwargs: Any,
    ) -> None:
        """
        Initialize configuration manager.

        Args:
            username: Upstream username
            password: Upstream password
            base_url: Base URL for Upstream API
            ckan_url: CKAN portal URL
            timeout: Request timeout in seconds
            max_retries: Maximum retry attempts
            chunk_size: Number of records per chunk
            max_chunk_size_mb: Maximum chunk size in MB
            **kwargs: Additional configuration options
        """
        # Load from environment variables first
        self.username = username or os.getenv("UPSTREAM_USERNAME")
        self.password = password or os.getenv("UPSTREAM_PASSWORD")
        self.base_url = base_url or os.getenv(
            "UPSTREAM_BASE_URL", "https://upstream-dso.tacc.utexas.edu/dev"
        )
        self.ckan_url = ckan_url or os.getenv(
            "CKAN_URL", "https://ckan.tacc.utexas.edu"
        )

        # Configuration options
        self.timeout = timeout
        self.max_retries = max_retries
        self.chunk_size = chunk_size
        self.max_chunk_size_mb = max_chunk_size_mb

        # Additional options
        self.extra_config = kwargs

        # Validate configuration
        self._validate()

    def _validate(self) -> None:
        """Validate configuration."""
        if not self.base_url:
            raise ConfigurationError("Base URL is required")

        if not self.base_url.startswith(("http://", "https://")):
            raise ConfigurationError("Base URL must start with http:// or https://")

        if self.ckan_url and not self.ckan_url.startswith(("http://", "https://")):
            raise ConfigurationError("CKAN URL must start with http:// or https://")

        if self.timeout <= 0:
            raise ConfigurationError("Timeout must be positive")

        if self.max_retries < 0:
            raise ConfigurationError("Max retries must be non-negative")

        if self.chunk_size <= 0:
            raise ConfigurationError("Chunk size must be positive")

        if self.max_chunk_size_mb <= 0:
            raise ConfigurationError("Max chunk size must be positive")

    @classmethod
    def from_file(cls, config_path: Union[str, Path]) -> "ConfigManager":
        """
        Load configuration from file.

        Args:
            config_path: Path to configuration file

        Returns:
            ConfigManager instance
        """
        config_path = Path(config_path)

        if not config_path.exists():
            raise ConfigurationError(f"Configuration file not found: {config_path}")

        try:
            with open(config_path, "r") as f:
                if config_path.suffix.lower() in [".yaml", ".yml"]:
                    config_data = yaml.safe_load(f)
                elif config_path.suffix.lower() == ".json":
                    config_data = json.load(f)
                else:
                    raise ConfigurationError(
                        f"Unsupported configuration file format: {config_path.suffix}"
                    )

            # Flatten nested configuration
            flattened_config = {}

            if "upstream" in config_data:
                flattened_config.update(config_data["upstream"])

            if "ckan" in config_data:
                ckan_config = config_data["ckan"]
                flattened_config["ckan_url"] = ckan_config.get("url")
                flattened_config.update(
                    {k: v for k, v in ckan_config.items() if k != "url"}
                )

            if "upload" in config_data:
                upload_config = config_data["upload"]
                flattened_config["chunk_size"] = upload_config.get("chunk_size", 10000)
                flattened_config["max_chunk_size_mb"] = upload_config.get(
                    "max_file_size_mb", 50
                )
                flattened_config["timeout"] = upload_config.get("timeout_seconds", 30)
                flattened_config["max_retries"] = upload_config.get("retry_attempts", 3)

            # Add any other top-level configuration
            for key, value in config_data.items():
                if key not in ["upstream", "ckan", "upload"]:
                    flattened_config[key] = value

            return cls(**flattened_config)

        except Exception as e:
            raise ConfigurationError(f"Failed to load configuration: {e}")

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert configuration to dictionary.

        Returns:
            Configuration dictionary
        """
        return {
            "username": self.username,
            "password": self.password,
            "base_url": self.base_url,
            "ckan_url": self.ckan_url,
            "timeout": self.timeout,
            "max_retries": self.max_retries,
            "chunk_size": self.chunk_size,
            "max_chunk_size_mb": self.max_chunk_size_mb,
            **self.extra_config,
        }

    def save(self, config_path: Union[str, Path]) -> None:
        """
        Save configuration to file.

        Args:
            config_path: Path to save configuration
        """
        config_path = Path(config_path)

        # Create configuration structure
        config_data = {
            "upstream": {
                "username": self.username,
                "password": self.password,
                "base_url": self.base_url,
            },
            "ckan": {
                "url": self.ckan_url,
            },
            "upload": {
                "chunk_size": self.chunk_size,
                "max_file_size_mb": self.max_chunk_size_mb,
                "timeout_seconds": self.timeout,
                "retry_attempts": self.max_retries,
            },
        }

        # Add extra configuration
        config_data.update(self.extra_config)

        try:
            with open(config_path, "w") as f:
                if config_path.suffix.lower() in [".yaml", ".yml"]:
                    yaml.dump(config_data, f, default_flow_style=False, indent=2)
                elif config_path.suffix.lower() == ".json":
                    json.dump(config_data, f, indent=2)
                else:
                    raise ConfigurationError(
                        f"Unsupported configuration file format: {config_path.suffix}"
                    )

            logger.info(f"Configuration saved to: {config_path}")

        except Exception as e:
            raise ConfigurationError(f"Failed to save configuration: {e}")


def setup_logging(
    level: str = "INFO",
    format_string: Optional[str] = None,
    filename: Optional[str] = None,
) -> None:
    """
    Setup logging configuration.

    Args:
        level: Logging level
        format_string: Custom format string
        filename: Log file path
    """
    if format_string is None:
        format_string = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    logging_config = {
        "level": getattr(logging, level.upper()),
        "format": format_string,
        "datefmt": "%Y-%m-%d %H:%M:%S",
    }

    if filename:
        logging_config["filename"] = filename

    logging.basicConfig(**logging_config)

    # Set specific loggers to appropriate levels
    logging.getLogger("requests").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)


def validate_file_size(file_path: Union[str, Path], max_size_mb: int = 100) -> bool:
    """
    Validate file size.

    Args:
        file_path: Path to file
        max_size_mb: Maximum file size in MB

    Returns:
        True if file size is valid
    """
    file_path = Path(file_path)

    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    file_size_mb = file_path.stat().st_size / (1024 * 1024)

    return file_size_mb <= max_size_mb


def chunk_file(
    file_path: Union[str, Path],
    chunk_size: int = 10000,
    max_chunk_size_mb: int = 50,
) -> list:
    """
    Split file into chunks.

    Args:
        file_path: Path to file
        chunk_size: Number of records per chunk
        max_chunk_size_mb: Maximum chunk size in MB

    Returns:
        List of chunk file paths
    """
    import csv
    import tempfile

    file_path = Path(file_path)

    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    chunk_files = []

    with open(file_path, "r", newline="", encoding="utf-8") as input_file:
        reader = csv.reader(input_file)
        header = next(reader)

        chunk_num = 0
        current_chunk_size = 0
        current_chunk_file = None
        current_chunk_writer = None

        for row in reader:
            # Start new chunk if needed
            if current_chunk_file is None or current_chunk_size >= chunk_size:
                if current_chunk_file is not None:
                    current_chunk_file.close()

                chunk_num += 1
                temp_file = tempfile.NamedTemporaryFile(
                    mode="w",
                    suffix=f"_chunk_{chunk_num}.csv",
                    delete=False,
                    newline="",
                    encoding="utf-8",
                )

                current_chunk_file = temp_file
                current_chunk_writer = csv.writer(temp_file)
                current_chunk_writer.writerow(header)
                current_chunk_size = 0

                chunk_files.append(temp_file.name)

            current_chunk_writer.writerow(row)  # type: ignore
            current_chunk_size += 1

        if current_chunk_file is not None:
            current_chunk_file.close()

    return chunk_files


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance with consistent formatting.

    Args:
        name: Logger name (typically __name__)

    Returns:
        Configured logger instance
    """
    return logging.getLogger(name)


def format_timestamp(timestamp: Optional[datetime]) -> Optional[str]:
    """
    Format datetime object to ISO 8601 string.

    Args:
        timestamp: Datetime object to format

    Returns:
        ISO 8601 formatted string or None if input is None
    """
    if timestamp is None:
        return None
    return timestamp.isoformat()


def parse_timestamp(timestamp_str: str) -> Optional[datetime]:
    """
    Parse ISO 8601 timestamp string to datetime object.

    Args:
        timestamp_str: ISO 8601 formatted timestamp string

    Returns:
        Parsed datetime object or None if parsing fails
    """
    from dateutil.parser import parse

    if not timestamp_str:
        return None

    try:
        return parse(timestamp_str)
    except (ValueError, TypeError) as e:
        logger.warning(f"Failed to parse timestamp '{timestamp_str}': {e}")
        return None
