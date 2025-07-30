"""
Data types and structures for the OHLCV to Orderbook conversion.
"""
from dataclasses import dataclass
from typing import List


@dataclass
class ValidationResult:
    """Result of a validation operation."""
    is_valid: bool
    warnings: List[str]
    errors: List[str]

    def __post_init__(self) -> None:
        """Ensure warnings and errors are lists."""
        if self.warnings is None:
            self.warnings = []
        if self.errors is None:
            self.errors = []


@dataclass
class ValidationConfig:
    """Configuration for validation operations."""
    price_tolerance: float = 0.01  # 1% default tolerance
    volume_tolerance: float = 0.30  # 30% default tolerance
    min_spread: float = 0.0001  # 0.01% minimum spread
    max_spread: float = 0.05  # 5% maximum spread

    def __post_init__(self) -> None:
        """Validate configuration values."""
        if self.price_tolerance < 0:
            raise ValueError("Price tolerance must be non-negative")
        if self.volume_tolerance < 0:
            raise ValueError("Volume tolerance must be non-negative")
