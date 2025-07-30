"""
Module for generating synthetic orderbook data from OHLCV.
"""
import argparse
import logging
from datetime import datetime
from pathlib import Path
from typing import Union, Optional, Tuple, List, Any, Dict

import numpy as np
import pandas as pd
import numpy.typing as npt

from .config import OrderbookConfig
from .exceptions import ValidationError, OrderbookGenerationError
from .io_handlers import ParquetHandler
from .data_types import ValidationResult, ValidationConfig

logger = logging.getLogger(__name__)


class OrderbookGenerator:
    """Generates synthetic orderbook data from OHLCV."""

    def __init__(
        self,
        config: Optional[OrderbookConfig] = None,
        validate_data: bool = True
    ) -> None:
        """
        Initialize the generator with customizable configuration.

        Args:
            config: Configuration for orderbook generation
            validate_data: If True, validate input/output data
        """
        self.config = config or OrderbookConfig()
        self.validate_data = validate_data
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

    def _validate_ohlcv(self, data: pd.DataFrame) -> None:
        """
        Validate input OHLCV data.

        Raises:
            ValidationError: If data is not valid
        """
        if not all(col in data.columns for col in ['timestamp', 'open', 'high', 'low', 'close', 'volume']):
            raise ValidationError("Missing OHLCV columns in DataFrame")

        if (data.high < data.low).any():
            raise ValidationError("High prices lower than low prices")

        if ((data.open < data.low) | (data.open > data.high)).any():
            raise ValidationError("Open prices outside high-low range")

        if ((data.close < data.low) | (data.close > data.high)).any():
            raise ValidationError("Close prices outside high-low range")

        if (data.volume <= 0).any():
            raise ValidationError("Non-positive volumes")

    def load_ohlcv_data(self, file_path: Union[str, Path]) -> pd.DataFrame:
        """
        Load OHLCV data from Parquet file with validation.

        Args:
            file_path: File path

        Returns:
            DataFrame with OHLCV data

        Raises:
            OrderbookGenerationError: If there are loading problems
        """
        try:
            return self.io_handler.read_parquet(file_path)
        except Exception as e:
            raise OrderbookGenerationError(f"Error loading OHLCV: {e}") from e

    def save_orderbook_data(self, orderbook_df: pd.DataFrame, output_path: str) -> None:
        """
        Save orderbook data to file using ParquetHandler

        Args:
            orderbook_df: DataFrame with orderbook data
            output_path: Path where to save the file
        """
        self.io_handler.write_parquet(orderbook_df, output_path)

    def calculate_spread(self, close_price: float, volatility: float) -> float:
        """
        Calculate the bid-ask spread based on price and volatility

        Args:
            close_price: Close price of the bar
            volatility: Volatility estimate

        Returns:
            Calculated spread
        """
        base_spread = close_price * self.config.spread_percentage
        volatility_adjustment = 1 + (volatility * 2)
        return base_spread * volatility_adjustment

    def estimate_price_path(self, open_price: float, high_price: float, low_price: float, close_price: float) -> npt.NDArray[np.float64]:
        """
        Public method to estimate the price path (for testing).

        Args:
            open_price: Open price
            high_price: High price
            low_price: Low price
            close_price: Close price

        Returns:
            Numpy array with the estimated price path
        """
        # Create a temporary Series to reuse the private method
        row = pd.Series({
            'open': open_price,
            'high': high_price,
            'low': low_price,
            'close': close_price
        })
        return self._estimate_price_path(row)

    def _estimate_price_path(self, row: "pd.Series[Any]") -> npt.NDArray[np.float64]:
        """
        Estimate the price path within an OHLCV bar.

        Args:
            row: DataFrame row with OHLCV data

        Returns:
            Numpy array with the estimated price path
        """
        open_price = float(row['open'])
        high_price = float(row['high'])
        low_price = float(row['low'])
        close_price = float(row['close'])

        # Simulate a realistic path: O -> H/L -> C
        # Decide whether to hit high or low first
        if abs(high_price - open_price) > abs(low_price - open_price):
            # Hit low first, then high
            path = [open_price, low_price, high_price, close_price]
        else:
            # Hit high first, then low
            path = [open_price, high_price, low_price, close_price]

        return np.array(path, dtype=np.float64)

    def _calculate_dynamic_spread_and_sizes(
        self,
        current_price: float,
        price_path: np.ndarray,
        position_in_path: float,
        total_volume: float,
        volatility: float
    ) -> Tuple[float, float, float]:
        """
        Calculate dynamically adjusted spread and sizes based on position in price path

        Args:
            current_price: Current price point
            price_path: Complete price path for the bar
            position_in_path: Current position in path (0-1)
            total_volume: Total volume for the bar
            volatility: Bar volatility

        Returns:
            Tuple of (spread, bid_size, ask_size) with dynamic adjustments
        """
        path_length = len(price_path)
        current_idx = int(position_in_path * (path_length - 1))
        if current_idx < path_length - 1:
            next_price = price_path[current_idx + 1]
            price_direction = (next_price - current_price) / current_price if current_price != 0 else 0
        else:
            price_direction = 0

        base_spread = current_price * self.config.spread_percentage
        volatility_multiplier = 1 + (volatility * 2)
        dynamic_spread = base_spread * volatility_multiplier

        # Correction: the base volume per point should maintain the total volume
        # multiplied by the distribution factor, not divided by the length of the path
        base_volume_per_point = (total_volume * self.config.size_distribution_factor) / path_length

        if price_direction > 0:
            ask_size = base_volume_per_point * (0.6 + abs(price_direction) * 2)
            bid_size = base_volume_per_point * (0.4 - abs(price_direction) * 0.5)
        elif price_direction < 0:
            bid_size = base_volume_per_point * (0.6 + abs(price_direction) * 2)
            ask_size = base_volume_per_point * (0.4 - abs(price_direction) * 0.5)
        else:
            bid_size = base_volume_per_point * 0.5
            ask_size = base_volume_per_point * 0.5

        return dynamic_spread, max(0.01, bid_size), max(0.01, ask_size)

    def generate_orderbook_data(
        self,
        ohlcv_df: pd.DataFrame,
        points_per_bar: Optional[int] = None
    ) -> pd.DataFrame:
        """
        Generate orderbook data from OHLCV using the estimated price path.

        Args:
            ohlcv_df: DataFrame with OHLCV data
            points_per_bar: Orderbook points per bar (override config)

        Returns:
            DataFrame with orderbook data

        Raises:
            OrderbookGenerationError: If there are problems in generation
        """
        try:
            points_per_bar = points_per_bar or self.config.points_per_bar
            orderbook_data = []

            logger.info(
                f"Generating orderbook from {len(ohlcv_df)} bars "
                f"({points_per_bar} points per bar)"
            )

            for idx, row in ohlcv_df.iterrows():
                try:
                    # Generate points for this bar
                    bar_points = self._generate_bar_points(
                        row, points_per_bar, idx
                    )
                    orderbook_data.extend(bar_points)
                except Exception as e:
                    logger.warning(
                        f"Error generating points for bar {idx}: {e}"
                    )
                    continue

            df = pd.DataFrame(orderbook_data)

            # Round values according to configuration if DataFrame is not empty
            if not df.empty:
                price_cols = ['bid_price', 'ask_price', 'mid_price']
                volume_cols = ['bid_size', 'ask_size']

                df[price_cols] = df[price_cols].round(self.config.price_decimals)
                df[volume_cols] = df[volume_cols].round(self.config.volume_decimals)

            logger.info(f"Generated {len(df)} orderbook points")
            return df

        except Exception as e:
            raise OrderbookGenerationError(
                f"Error generating orderbook: {e}"
            ) from e

    def generate_orderbook(
        self,
        ohlcv_df: pd.DataFrame,
        points_per_bar: Optional[int] = None
    ) -> pd.DataFrame:
        """
        Alias for generate_orderbook_data for backward compatibility.

        Args:
            ohlcv_df: DataFrame with OHLCV data
            points_per_bar: Orderbook points per bar (override config)

        Returns:
            DataFrame with orderbook data
        """
        return self.generate_orderbook_data(ohlcv_df, points_per_bar)

    def _generate_bar_points(
        self,
        row: "pd.Series[Any]",
        points_per_bar: int,
        timestamp_base: Any
    ) -> List[Dict[str, Any]]:
        """
        Generate orderbook points for a single OHLCV bar.

        Args:
            row: Row with OHLCV data
            points_per_bar: Number of points to generate
            timestamp_base: Base timestamp for the points

        Returns:
            List of dictionaries with orderbook data
        """
        price_path = self._estimate_price_path(row)
        total_volume = float(row['volume'])
        volatility = self._calculate_volatility(row)

        # Create incremental timestamps for each point within the bar
        base_timestamp = pd.to_datetime(row['timestamp'])
        time_increment = pd.Timedelta(seconds=60 // points_per_bar)  # Distributes over 1 minute

        points: List[Dict[str, Any]] = []
        for i in range(points_per_bar):
            position = i / (points_per_bar - 1) if points_per_bar > 1 else 0
            price_idx = int(position * (len(price_path) - 1))
            current_price = float(price_path[price_idx])

            spread, bid_size, ask_size = self._calculate_dynamic_spread_and_sizes(
                current_price, price_path, position, total_volume, volatility
            )

            bid_price = current_price - spread / 2
            ask_price = current_price + spread / 2
            mid_price = current_price

            # Incremental timestamp for each point
            point_timestamp = base_timestamp + (time_increment * i)

            point: Dict[str, Any] = {
                'timestamp': point_timestamp,
                'bid_price': bid_price,
                'ask_price': ask_price,
                'mid_price': mid_price,
                'bid_size': bid_size,
                'ask_size': ask_size
            }
            points.append(point)

        return points

    def _calculate_volatility(self, row: "pd.Series[Any]") -> float:
        """
        Calculate volatility for an OHLCV bar.

        Args:
            row: Row with OHLCV data

        Returns:
            Volatility estimate
        """
        high_low_range = (float(row['high']) - float(row['low'])) / float(row['close'])
        return float(high_low_range)

    def generate_summary_stats(self, orderbook_df: pd.DataFrame) -> Dict[str, Any]:
        """
        Generate summary statistics on orderbook data.

        Args:
            orderbook_df: DataFrame with orderbook data

        Returns:
            Dictionary with summary statistics
        """
        if orderbook_df.empty:
            return {
                'total_points': 0,
                'total_records': 0,
                'time_range': 'N/A',
                'price_range': 'N/A',
                'average_spread': 0,
                'avg_spread': 0,
                'avg_spread_percentage': 0,
                'total_volume': 0,
                'avg_bid_size': 0,
                'avg_ask_size': 0,
                'min_spread': 0,
                'max_spread': 0,
                'price_range': {
                    'min_bid': 0,
                    'max_ask': 0,
                    'min_mid': 0,
                    'max_mid': 0
                }
            }

        spread_values = orderbook_df['ask_price'] - orderbook_df['bid_price']
        avg_spread = spread_values.mean()
        avg_mid_price = orderbook_df['mid_price'].mean()

        stats = {
            'total_points': len(orderbook_df),
            'total_records': len(orderbook_df),
            'time_range': f"{orderbook_df['timestamp'].min()} to {orderbook_df['timestamp'].max()}",
            'price_range': f"{orderbook_df['mid_price'].min():.2f} - {orderbook_df['mid_price'].max():.2f}",
            'average_spread': avg_spread,
            'avg_spread': avg_spread,
            'avg_spread_percentage': (avg_spread / avg_mid_price * 100) if avg_mid_price > 0 else 0,
            'total_volume': orderbook_df['bid_size'].sum() + orderbook_df['ask_size'].sum(),
            'avg_bid_size': orderbook_df['bid_size'].mean(),
            'avg_ask_size': orderbook_df['ask_size'].mean(),
            'min_spread': spread_values.min(),
            'max_spread': spread_values.max(),
            'price_range': {
                'min_bid': orderbook_df['bid_price'].min(),
                'max_ask': orderbook_df['ask_price'].max(),
                'min_mid': orderbook_df['mid_price'].min(),
                'max_mid': orderbook_df['mid_price'].max()
            }
        }

        return stats


class OrderbookValidator:
    """
    Class to validate generated orderbook by reconstructing OHLCV bars and comparing with original data
    """

    def __init__(self, config: 'ValidationConfig'):
        """
        Initialize the validator

        Args:
            config: ValidationConfig object with tolerance settings
        """
        self.config = config
        self.tolerance_percentage = config.price_tolerance * 100  # Convert to percentage

    def validate_conversion(self, original_ohlcv: pd.DataFrame, orderbook_data: pd.DataFrame) -> 'ValidationResult':
        """
        Validate the conversion from OHLCV to orderbook.

        Args:
            original_ohlcv: Original OHLCV data
            orderbook_data: Generated orderbook data

        Returns:
            ValidationResult object with validation details
        """
        warnings: List[str] = []
        errors: List[str] = []

        # Basic validation checks
        if orderbook_data.empty:
            errors.append("Generated orderbook data is empty")
            return ValidationResult(is_valid=False, warnings=warnings, errors=errors)

        # Check required columns
        required_columns = ['timestamp', 'bid_price', 'bid_size', 'ask_price', 'ask_size']
        missing_columns = [col for col in required_columns if col not in orderbook_data.columns]
        if missing_columns:
            errors.append(f"Missing required columns: {missing_columns}")

        # Check for negative prices or sizes
        if (orderbook_data['bid_price'] <= 0).any() or (orderbook_data['ask_price'] <= 0).any():
            errors.append("Found non-positive prices in orderbook data")

        if (orderbook_data['bid_size'] <= 0).any() or (orderbook_data['ask_size'] <= 0).any():
            errors.append("Found non-positive sizes in orderbook data")

        # Check bid-ask spread validity
        spreads = orderbook_data['ask_price'] - orderbook_data['bid_price']
        if (spreads <= 0).any():
            errors.append("Found negative or zero spreads")

        # Check spread bounds
        avg_price = (orderbook_data['bid_price'] + orderbook_data['ask_price']) / 2
        spread_pct = spreads / avg_price

        if (spread_pct < self.config.min_spread).any():
            warnings.append(f"Some spreads are below minimum threshold ({self.config.min_spread*100:.2f}%)")

        if (spread_pct > self.config.max_spread).any():
            warnings.append(f"Some spreads are above maximum threshold ({self.config.max_spread*100:.2f}%)")

        # Volume validation
        total_orderbook_volume = orderbook_data['bid_size'].sum() + orderbook_data['ask_size'].sum()
        total_ohlcv_volume = original_ohlcv['volume'].sum()

        volume_diff_pct = abs(total_orderbook_volume - total_ohlcv_volume) / total_ohlcv_volume
        if volume_diff_pct > self.config.volume_tolerance:
            warnings.append(f"Total volume difference exceeds tolerance: {volume_diff_pct*100:.2f}%")

        is_valid = len(errors) == 0
        return ValidationResult(is_valid=is_valid, warnings=warnings, errors=errors)

    def reconstruct_ohlcv_from_orderbook(self, orderbook_df: pd.DataFrame, points_per_bar: int = 4) -> pd.DataFrame:
        """
        Reconstruct OHLCV bars from orderbook data

        Args:
            orderbook_df: DataFrame with orderbook data
            points_per_bar: Number of points per original bar

        Returns:
            DataFrame with reconstructed OHLCV bars
        """
        reconstructed_bars = []
        total_points = len(orderbook_df)
        num_bars = total_points // points_per_bar
        for bar_idx in range(num_bars):
            start_idx = bar_idx * points_per_bar
            end_idx = start_idx + points_per_bar
            bar_points = orderbook_df.iloc[start_idx:end_idx]
            if len(bar_points) == 0:
                continue
            mid_prices_series = bar_points['mid_price']
            mid_prices = mid_prices_series.to_numpy()
            sizes = bar_points[['bid_size', 'ask_size']].sum(axis=1).to_numpy()
            reconstructed_bar = {
                'open': float(mid_prices[0]),
                'high': float(mid_prices.max()),
                'low': float(mid_prices.min()),
                'close': float(mid_prices[-1]),
                'volume': float(sizes.sum()),
                'bar_index': bar_idx,
                'timestamp': bar_points.iloc[0]['timestamp'],
                'num_points': len(bar_points)
            }
            reconstructed_bars.append(reconstructed_bar)
        return pd.DataFrame(reconstructed_bars)

    def compare_ohlcv_data(self, original_df: pd.DataFrame, reconstructed_df: pd.DataFrame) -> Dict[str, Any]:
        """
        Compare original OHLCV data with reconstructed OHLCV

        Args:
            original_df: Original OHLCV DataFrame
            reconstructed_df: Reconstructed OHLCV DataFrame

        Returns:
            Dictionary with comparison results
        """
        comparison_results: Dict[str, Any] = {
            'total_bars_original': len(original_df),
            'total_bars_reconstructed': len(reconstructed_df),
            'comparison_details': [],
            'summary_stats': {},
            'validation_passed': True,
            'errors': []
        }
        if len(original_df) != len(reconstructed_df):
            error_msg = f"Different number of bars: {len(original_df)} vs {len(reconstructed_df)}"
            comparison_results['errors'].append(error_msg)
            comparison_results['validation_passed'] = False
        min_bars = min(len(original_df), len(reconstructed_df))
        price_columns = ['open', 'high', 'low', 'close']
        volume_columns = ['volume']
        differences: Dict[str, List[float]] = {col: [] for col in price_columns + volume_columns}
        for i in range(min_bars):
            original_bar = original_df.iloc[i]
            reconstructed_bar = reconstructed_df.iloc[i]
            bar_comparison: Dict[str, Any] = {
                'bar_index': i,
                'original': {},
                'reconstructed': {},
                'differences': {},
                'percentage_differences': {},
                'within_tolerance': {}
            }
            for col in price_columns + volume_columns:
                if col in original_bar and col in reconstructed_bar:
                    orig_val = original_bar[col]
                    recon_val = reconstructed_bar[col]
                    bar_comparison['original'][col] = orig_val
                    bar_comparison['reconstructed'][col] = recon_val
                    abs_diff = abs(orig_val - recon_val)
                    pct_diff: float = float((abs_diff / orig_val * 100) if orig_val != 0 else 0)
                    bar_comparison['differences'][col] = abs_diff
                    bar_comparison['percentage_differences'][col] = pct_diff
                    bar_comparison['within_tolerance'][col] = pct_diff <= self.tolerance_percentage
                    differences[col].append(pct_diff)
                    if pct_diff > self.tolerance_percentage:
                        error_msg = f"Bar {i}, {col}: difference {pct_diff:.4f}% > tolerance {self.tolerance_percentage}%"
                        comparison_results['errors'].append(error_msg)
                        comparison_results['validation_passed'] = False
            comparison_results['comparison_details'].append(bar_comparison)
        for col in differences:
            if differences[col]:
                comparison_results['summary_stats'][col] = {
                    'mean_difference_pct': np.mean(differences[col]),
                    'max_difference_pct': np.max(differences[col]),
                    'min_difference_pct': np.min(differences[col]),
                    'std_difference_pct': np.std(differences[col]),
                    'bars_within_tolerance': sum(1 for d in differences[col] if d <= self.tolerance_percentage),
                    'bars_outside_tolerance': sum(1 for d in differences[col] if d > self.tolerance_percentage)
                }
        return comparison_results

    def generate_validation_report(self, comparison_results: Dict[str, Any], save_path: Optional[str] = None) -> str:
        """
        Generate a detailed validation report

        Args:
            comparison_results: Comparison results
            save_path: Path to save the report (optional)

        Returns:
            String with the report
        """
        report = []
        report.append("=" * 60)
        report.append("ORDERBOOK VALIDATION REPORT")
        report.append("=" * 60)
        status = "✅ PASSED" if comparison_results['validation_passed'] else "❌ FAILED"
        report.append(f"Status: {status}")
        report.append(f"Tolerance: {self.tolerance_percentage}%")
        report.append("")
        report.append("GENERAL STATS:")
        report.append(f"- Original bars: {comparison_results['total_bars_original']}")
        report.append(f"- Reconstructed bars: {comparison_results['total_bars_reconstructed']}")
        report.append(f"- Total errors: {len(comparison_results['errors'])}")
        report.append("")
        if comparison_results['summary_stats']:
            report.append("COLUMN DIFFERENCE STATS:")
            for col, stats in comparison_results['summary_stats'].items():
                report.append(f"\n{col.upper()}:")
                report.append(f"  - Mean difference: {stats['mean_difference_pct']:.4f}%")
                report.append(f"  - Max difference: {stats['max_difference_pct']:.4f}%")
                report.append(f"  - Min difference: {stats['min_difference_pct']:.4f}%")
                report.append(f"  - Std deviation: {stats['std_difference_pct']:.4f}%")
                report.append(f"  - Bars within tolerance: {stats['bars_within_tolerance']}")
                report.append(f"  - Bars outside tolerance: {stats['bars_outside_tolerance']}")
        if comparison_results['errors']:
            report.append("\nFIRST 10 ERRORS:")
            for error in comparison_results['errors'][:10]:
                report.append(f"  - {error}")
            if len(comparison_results['errors']) > 10:
                report.append(f"  ... and {len(comparison_results['errors']) - 10} more errors")
        if comparison_results['comparison_details']:
            report.append("\nFIRST 5 BAR DETAILS:")
            for i, detail in enumerate(comparison_results['comparison_details'][:5]):
                report.append(f"\nBar {detail['bar_index']}:")
                for col in ['open', 'high', 'low', 'close', 'volume']:
                    if col in detail['original']:
                        orig = detail['original'][col]
                        recon = detail['reconstructed'][col]
                        diff_pct = detail['percentage_differences'][col]
                        tolerance_ok = "✅" if detail['within_tolerance'][col] else "❌"
                        report.append(f"  {col}: {orig:.6f} → {recon:.6f} ({diff_pct:.4f}%) {tolerance_ok}")
        report_text = "\n".join(report)
        if save_path:
            try:
                with open(save_path, 'w', encoding='utf-8') as f:
                    f.write(report_text)
                print(f"Report saved to: {save_path}")
            except Exception as e:
                print(f"Error saving report: {e}")
        return report_text

    def run_full_validation(self, original_ohlcv_df: pd.DataFrame, orderbook_df: pd.DataFrame, points_per_bar: int = 4, report_path: Optional[str] = None) -> Tuple[bool, Dict[str, Any], str]:
        """
        Run a full orderbook validation

        Args:
            original_ohlcv_df: Original OHLCV DataFrame
            orderbook_df: Generated orderbook DataFrame
            points_per_bar: Points per bar
            report_path: Path to save report

        Returns:
            Tuple (validation_passed, comparison_results, report_text)
        """
        print("Reconstructing OHLCV bars from orderbook...")
        reconstructed_df = self.reconstruct_ohlcv_from_orderbook(orderbook_df, points_per_bar)
        print("Comparing with original data...")
        comparison_results = self.compare_ohlcv_data(original_ohlcv_df, reconstructed_df)
        print("Generating report...")
        report_text = self.generate_validation_report(comparison_results, report_path)
        return comparison_results['validation_passed'], comparison_results, report_text


def main() -> None:
    parser = argparse.ArgumentParser(
        description='Generate L1 orderbook data from OHLCV parquet file using estimated price path')
    parser.add_argument('input_file', help='Parquet file with OHLCV data')
    parser.add_argument('-o', '--output', default='orderbook_data.parquet',
                        help='Output file (default: orderbook_data.parquet)')
    parser.add_argument('-s', '--spread', type=float, default=0.001,
                        help='Base spread percentage (default: 0.001 = 0.1%%)')
    parser.add_argument('-v', '--size-factor', type=float, default=0.3,
                        help='Size distribution factor (default: 0.3)')
    parser.add_argument('-p', '--points-per-bar', type=int, default=4,
                        help='Orderbook points per OHLC bar (default: 4)')
    parser.add_argument('--stats', action='store_true',
                        help='Show summary statistics')
    parser.add_argument('--validate', action='store_true',
                        help='Run validation by reconstructing OHLCV')
    parser.add_argument('--tolerance', type=float, default=0.1,
                        help='Tolerance percentage for validation (default: 0.1%%)')
    parser.add_argument('--report', type=str, default=None,
                        help='Save validation report to file')
    args = parser.parse_args()

    # Create configuration with correct parameters
    config = OrderbookConfig(
        spread_percentage=args.spread,
        size_distribution_factor=args.size_factor,
        points_per_bar=args.points_per_bar
    )
    generator = OrderbookGenerator(config=config)

    print(f"Loading data from: {args.input_file}")
    ohlcv_df = generator.load_ohlcv_data(args.input_file)
    if ohlcv_df is None:
        print("Error loading data. Exiting.")
        return
    print(f"Loaded {len(ohlcv_df)} OHLCV records")
    print(f"Generating {args.points_per_bar} orderbook points per bar...")
    print("Generating orderbook data using estimated price path...")
    orderbook_df = generator.generate_orderbook_data(ohlcv_df, points_per_bar=args.points_per_bar)
    generator.save_orderbook_data(orderbook_df, args.output)

    if args.stats:
        print("\n--- ORDERBOOK STATISTICS ---")
        stats = generator.generate_summary_stats(orderbook_df)
        print(f"Total records: {stats['total_records']}")
        print(f"Points per original bar: {stats['total_records'] // len(ohlcv_df)}")
        print(f"Mean spread: {stats['avg_spread']:.8f}")
        print(f"Mean spread %: {stats['avg_spread_percentage']:.4f}%")
        print(f"Mean bid size: {stats['avg_bid_size']:.2f}")
        print(f"Mean ask size: {stats['avg_ask_size']:.2f}")
        print(f"Spread range: {stats['min_spread']:.8f} - {stats['max_spread']:.8f}")
        print(f"\nPrice range:")
        print(f"  Bid: {stats['price_range']['min_bid']:.8f} - {stats['price_range']['max_ask']:.8f}")
        print(f"  Mid: {stats['price_range']['min_mid']:.8f} - {stats['price_range']['max_mid']:.8f}")
        if 'price_direction' in orderbook_df.columns:
            direction_counts = orderbook_df['price_direction'].value_counts()
            print(f"\nPrice direction distribution:")
            for direction, count in direction_counts.items():
                percentage = (count / len(orderbook_df)) * 100
                print(f"  {direction}: {count} ({percentage:.1f}%)")
    if args.validate:
        print("\n" + "=" * 50)
        print("ORDERBOOK VALIDATION")
        print("=" * 50)
        validation_config = ValidationConfig(price_tolerance=args.tolerance/100)  # Convert percentage to decimal
        validator = OrderbookValidator(config=validation_config)
        validation_passed, comparison_results, report_text = validator.run_full_validation(
            ohlcv_df, orderbook_df, args.points_per_bar, args.report
        )
        print(report_text)
        if validation_passed:
            print(f"\n✅ VALIDATION PASSED! Orderbook generated correctly.")
        else:
            print(f"\n❌ VALIDATION FAILED! Check the report for details.")
            print(f"Errors found: {len(comparison_results['errors'])}")
    print(f"\nDone! Orderbook data available at: {args.output}")
    print(f"Generated {len(orderbook_df)} orderbook points from {len(ohlcv_df)} OHLCV bars")


if __name__ == "__main__":
    main()
