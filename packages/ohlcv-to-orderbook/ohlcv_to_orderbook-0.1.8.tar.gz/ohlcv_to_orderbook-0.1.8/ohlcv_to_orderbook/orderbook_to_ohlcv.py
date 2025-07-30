"""
Module for reconstructing OHLCV data from level 1 orderbook.
"""
import argparse
import logging
from typing import Optional, Dict, Any

import numpy as np
import pandas as pd

from .config import OrderbookConfig
from .exceptions import ValidationError, ConversionError
from .io_handlers import ParquetHandler

logger = logging.getLogger(__name__)


class OHLCVGenerator:
    """Generates OHLCV data from level 1 orderbook."""

    def __init__(
        self,
        config: Optional[OrderbookConfig] = None,
        validate_data: bool = True,
        size_distribution_factor: Optional[float] = None
    ) -> None:
        """
        Initialize the generator with customizable configuration.

        Args:
            config: Configuration for OHLCV generation
            validate_data: If True, validate input/output data
            size_distribution_factor: Volume distribution factor used in orderbook generation.
                                    If provided, will be used to compensate volumes during reconstruction.
        """
        self.config = config or OrderbookConfig()
        self.validate_data = validate_data
        self.size_distribution_factor = size_distribution_factor
        self.io_handler = ParquetHandler()
        self._setup_logging()

    def _setup_logging(self) -> None:
        """Configure logging for the module"""
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)

    def _validate_orderbook(self, data: pd.DataFrame) -> None:
        """
        Validate input orderbook data.

        Raises:
            ValidationError: If data is not valid
        """
        required_columns = ['timestamp', 'bid_price', 'ask_price', 'bid_size', 'ask_size']
        if not all(col in data.columns for col in required_columns):
            raise ValidationError("Missing orderbook columns in DataFrame")

        if (data.bid_price >= data.ask_price).any():
            raise ValidationError("Bid prices greater than or equal to ask prices")

        if (data.bid_size <= 0).any() or (data.ask_size <= 0).any():
            raise ValidationError("Non-positive volumes")

    def generate_ohlcv_data(
        self,
        orderbook_df: pd.DataFrame,
        points_per_bar: Optional[int] = None
    ) -> pd.DataFrame:
        """
        Generate OHLCV data from orderbook using average prices.

        Args:
            orderbook_df: DataFrame with orderbook data
            points_per_bar: Orderbook points per bar (override config)

        Returns:
            DataFrame with OHLCV data

        Raises:
            ConversionError: If there are problems in generation
        """
        try:
            if self.validate_data:
                self._validate_orderbook(orderbook_df)

            points_per_bar = points_per_bar or self.config.points_per_bar

            # Calculate the average price for each point
            if 'mid_price' not in orderbook_df.columns:
                orderbook_df = orderbook_df.copy()
                orderbook_df['mid_price'] = (orderbook_df['bid_price'] + orderbook_df['ask_price']) / 2

            orderbook_df['total_volume'] = orderbook_df['bid_size'] + orderbook_df['ask_size']

            # Group data into bars
            grouped = orderbook_df.groupby(np.arange(len(orderbook_df)) // points_per_bar)

            ohlcv_data = []
            for _, group in grouped:
                if len(group) == 0:
                    continue

                bar = {
                    'timestamp': group['timestamp'].iloc[0],
                    'open': group['mid_price'].iloc[0],
                    'high': group['mid_price'].max(),
                    'low': group['mid_price'].min(),
                    'close': group['mid_price'].iloc[-1],
                    'volume': group['total_volume'].sum(),
                    'num_points': len(group)
                }
                ohlcv_data.append(bar)

            df = pd.DataFrame(ohlcv_data)

            # Compensate volumes if size_distribution_factor is provided
            if self.size_distribution_factor is not None:
                df['volume'] = df['volume'] / self.size_distribution_factor

            # Round values according to configuration
            price_cols = ['open', 'high', 'low', 'close']
            df[price_cols] = df[price_cols].round(self.config.price_decimals)
            df['volume'] = df['volume'].round(self.config.volume_decimals)

            # Remove internal columns that should not be in the final output
            columns_to_remove = ['num_points']
            for col in columns_to_remove:
                if col in df.columns:
                    df = df.drop(columns=[col])

            logger.info(f"Generated {len(df)} OHLCV bars")
            return df

        except Exception as e:
            raise ConversionError(f"Error generating OHLCV: {e}") from e

    def group_orderbook_to_bars(
        self,
        orderbook_df: pd.DataFrame,
        points_per_bar: Optional[int] = None
    ) -> pd.DataFrame:
        """
        Alias for generate_ohlcv_data for compatibility with tests.

        Args:
            orderbook_df: DataFrame with orderbook data
            points_per_bar: Orderbook points per bar

        Returns:
            DataFrame with OHLCV data
        """
        return self.generate_ohlcv_data(orderbook_df, points_per_bar)

    def generate_ohlcv(
        self,
        orderbook_df: pd.DataFrame,
        points_per_bar: Optional[int] = None
    ) -> pd.DataFrame:
        """
        Alias for generate_ohlcv_data for backward compatibility.

        Args:
            orderbook_df: DataFrame with orderbook data
            points_per_bar: Orderbook points per bar

        Returns:
            DataFrame with OHLCV data
        """
        return self.generate_ohlcv_data(orderbook_df, points_per_bar)

    def generate_summary_stats(self, ohlcv_df: pd.DataFrame) -> Dict[str, Any]:
        """
        Generate summary statistics for OHLCV data.

        Args:
            ohlcv_df: DataFrame with OHLCV data

        Returns:
            Dictionary with statistics:
                - total_bars: Total number of bars
                - avg_volume: Average volume
                - price_range: Dict with min/max prices
                - avg_bar_return: Average return per bar
                - volatility: Average volatility (high-low)/open
        """
        ohlcv_df['bar_return'] = (
            ohlcv_df['close'] - ohlcv_df['open']
        ) / ohlcv_df['open']
        ohlcv_df['volatility'] = (
            ohlcv_df['high'] - ohlcv_df['low']
        ) / ohlcv_df['open']

        stats = {
            'total_bars': len(ohlcv_df),
            'avg_volume': ohlcv_df['volume'].mean(),
            'price_range': {
                'min_price': ohlcv_df[['open', 'high', 'low', 'close']].min().min(),
                'max_price': ohlcv_df[['open', 'high', 'low', 'close']].max().max()
            },
            'avg_bar_return': ohlcv_df['bar_return'].mean(),
            'volatility': {
                'mean': ohlcv_df['volatility'].mean(),
                'min': ohlcv_df['volatility'].min(),
                'max': ohlcv_df['volatility'].max()
            }
        }
        return stats


def main() -> None:
    parser = argparse.ArgumentParser(
        description='Generate OHLCV data from L1 orderbook parquet file')
    parser.add_argument('input_file', help='Parquet file with orderbook data')
    parser.add_argument('-o', '--output', default='ohlcv_data.parquet',
                      help='Output file (default: ohlcv_data.parquet)')
    parser.add_argument('-p', '--points-per-bar', type=int, default=4,
                      help='Orderbook points per OHLC bar (default: 4)')
    parser.add_argument('--stats', action='store_true',
                      help='Show summary statistics')
    args = parser.parse_args()

    generator = OHLCVGenerator()
    print(f"Loading data from: {args.input_file}")
    orderbook_df = generator.io_handler.read_parquet(args.input_file)

    print(f"Loaded {len(orderbook_df)} orderbook records")
    print(f"Generating OHLCV bars from {args.points_per_bar} points each...")

    ohlcv_df = generator.generate_ohlcv_data(
        orderbook_df,
        points_per_bar=args.points_per_bar
    )

    generator.io_handler.write_parquet(ohlcv_df, args.output)

    if args.stats:
        print("\n--- OHLCV STATISTICS ---")
        stats = generator.generate_summary_stats(ohlcv_df)
        print(f"Total bars: {stats['total_bars']}")
        print(f"Points per bar: {len(orderbook_df) // stats['total_bars']}")
        print(f"Mean volume: {stats['avg_volume']:.2f}")
        print(f"Mean bar return: {stats['avg_bar_return']:.4%}")
        print(f"\nPrice range:")
        print(f"  Min: {stats['price_range']['min_price']:.8f}")
        print(f"  Max: {stats['price_range']['max_price']:.8f}")
        print(f"\nVolatility:")
        print(f"  Mean: {stats['volatility']['mean']:.4%}")
        print(f"  Range: {stats['volatility']['min']:.4%} - {stats['volatility']['max']:.4%}")

    print(f"\nDone! OHLCV data available at: {args.output}")
    print(f"Generated {len(ohlcv_df)} OHLCV bars from {len(orderbook_df)} orderbook points")
