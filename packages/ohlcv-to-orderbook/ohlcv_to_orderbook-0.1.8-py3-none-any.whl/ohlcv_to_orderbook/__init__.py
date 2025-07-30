"""
Package ohlcv_to_orderbook.
"""

try:
    from ._version import __version__
except ImportError:
    # Fallback for development installations
    __version__ = "unknown"

from .ohlcv_to_orderbook import OrderbookGenerator, OrderbookValidator
from .orderbook_to_ohlcv import OHLCVGenerator
from .synthetic_data import generate_test_data

__all__ = ['OrderbookGenerator', 'OHLCVGenerator', 'OrderbookValidator', 'generate_test_data', '__version__']
