"""
Custom exceptions for the project.
"""
from typing import Optional, Dict, Any


class BaseError(Exception):
    """Base exception class for the project."""
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message)
        self.details = details or {}


class ValidationError(BaseError):
    """Raised when data validation fails."""
    pass


class ConversionError(BaseError):
    """Raised when data conversion fails."""
    pass


class IOError(BaseError):
    """Raised when input/output operations fail."""
    pass


class OrderbookGenerationError(BaseError):
    """Raised when orderbook generation fails."""
    pass
