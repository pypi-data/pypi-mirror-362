"""
Centralized configuration for the project.
"""
from dataclasses import dataclass
from typing import Dict, Any, Optional


@dataclass
class OrderbookConfig:
    """Configuration for orderbook generation"""
    spread_percentage: float = 0.001  # 0.1% default spread
    size_distribution_factor: float = 0.3  # Volume distribution factor
    points_per_bar: int = 4  # Orderbook points per OHLCV bar
    price_decimals: int = 8  # Decimals for prices
    volume_decimals: int = 8  # Decimals for volumes


@dataclass
class IOConfig:
    """Configuration for input/output"""
    compression: str = 'snappy'  # Compression for parquet files
    row_group_size: int = 100000  # Size of parquet row groups


# Default configuration
DEFAULT_CONFIG = {
    'orderbook': OrderbookConfig(),
    'io': IOConfig(),
}


def load_config(config_dict: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Load configuration, combining default values with provided ones.

    Args:
        config_dict: Optional dictionary with custom configuration

    Returns:
        Complete configuration
    """
    if config_dict is None:
        return DEFAULT_CONFIG

    config = DEFAULT_CONFIG.copy()

    # Update only provided values
    for section, values in config_dict.items():
        if section in config:
            if isinstance(values, dict):
                current = config[section].__dict__.copy()
                current.update(values)
                config[section] = type(config[section])(**current)
            else:
                config[section] = values

    return config
