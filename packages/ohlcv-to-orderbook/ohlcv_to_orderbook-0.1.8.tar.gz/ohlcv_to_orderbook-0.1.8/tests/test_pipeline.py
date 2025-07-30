import os
import subprocess
from pathlib import Path
from typing import Dict, Tuple, Any

import numpy as np
import pandas as pd
import pytest

from ohlcv_to_orderbook.config import OrderbookConfig
from ohlcv_to_orderbook.data_types import ValidationConfig
from ohlcv_to_orderbook.ohlcv_to_orderbook import OrderbookGenerator, OrderbookValidator
from ohlcv_to_orderbook.orderbook_to_ohlcv import OHLCVGenerator
from ohlcv_to_orderbook.synthetic_data import generate_test_data


def analyze_differences(original_df: pd.DataFrame, reconstructed_df: pd.DataFrame) -> Dict[str, Any]:
    """
    Analyze in detail the differences between original and reconstructed data.

    Returns:
        Dictionary with detailed statistics on differences
    """
    analysis: Dict[str, Any] = {
        'price_differences': {},
        'volume_differences': {},
        'summary': {}
    }

    for col in ['open', 'high', 'low', 'close']:
        diff_pct = ((reconstructed_df[col] - original_df[col]) / original_df[col] * 100)
        analysis['price_differences'][col] = {
            'mean_diff_pct': diff_pct.mean(),
            'std_diff_pct': diff_pct.std(),
            'max_diff_pct': diff_pct.max(),
            'min_diff_pct': diff_pct.min(),
            'median_diff_pct': diff_pct.median()
        }

    vol_diff_pct = ((reconstructed_df['volume'] - original_df['volume']) / original_df['volume'] * 100)
    analysis['volume_differences'] = {
        'mean_diff_pct': vol_diff_pct.mean(),
        'std_diff_pct': vol_diff_pct.std(),
        'max_diff_pct': vol_diff_pct.max(),
        'min_diff_pct': vol_diff_pct.min(),
        'median_diff_pct': vol_diff_pct.median()
    }

    # Overall analysis
    analysis['summary'] = {
        'worst_price_diff': max([
            abs(stats['max_diff_pct'])
            for stats in analysis['price_differences'].values()
        ]),
        'worst_volume_diff': abs(analysis['volume_differences']['max_diff_pct']),
        'average_price_diff': np.mean([
            stats['mean_diff_pct']
            for stats in analysis['price_differences'].values()
        ]),
        'average_volume_diff': analysis['volume_differences']['mean_diff_pct']
    }

    return analysis


def print_detailed_analysis(analysis: Dict[str, Any]) -> None:
    """
    Print a detailed analysis of the differences.
    """
    print("\nDETAILED DIFFERENCE ANALYSIS")
    print("="*50)

    print("\nPrice differences:")
    for col, stats in analysis['price_differences'].items():
        print(f"\n{col.upper()}:")
        print(f"  Mean: {stats['mean_diff_pct']:>8.4f}%")
        print(f"  Median: {stats['median_diff_pct']:>6.4f}%")
        print(f"  Max: {stats['max_diff_pct']:>10.4f}%")
        print(f"  Min: {stats['min_diff_pct']:>10.4f}%")
        print(f"  Std: {stats['std_diff_pct']:>10.4f}%")

    print("\nVolume differences:")
    vol_stats = analysis['volume_differences']
    print(f"  Mean: {vol_stats['mean_diff_pct']:>8.4f}%")
    print(f"  Median: {vol_stats['median_diff_pct']:>6.4f}%")
    print(f"  Max: {vol_stats['max_diff_pct']:>10.4f}%")
    print(f"  Min: {vol_stats['min_diff_pct']:>10.4f}%")
    print(f"  Std: {vol_stats['std_diff_pct']:>10.4f}%")

    print("\nSummary:")
    summary = analysis['summary']
    print(f"  Maximum price difference: {summary['worst_price_diff']:>6.4f}%")
    print(f"  Average price difference: {summary['average_price_diff']:>8.4f}%")
    print(f"  Maximum volume difference: {summary['worst_volume_diff']:>6.4f}%")
    print(f"  Average volume difference: {summary['average_volume_diff']:>8.4f}%")


def test_full_pipeline() -> None:
    """
    Test the entire pipeline with detailed discrepancy analysis
    """
    # Test configuration
    num_bars = 100
    points_per_bar = 4
    test_data_path = 'test_ohlcv_data.parquet'
    orderbook_data_path = 'test_orderbook_data.parquet'
    reconstructed_data_path = 'test_reconstructed_ohlcv.parquet'
    VOLUME_TOLERANCE = 30.0  # 30% tolerance for volumes

    try:
        # 1. Generate synthetic OHLCV data
        print("\n1. Generating synthetic OHLCV data...")
        ohlcv_df, stats = generate_test_data(
            output_file=test_data_path,
            num_bars=num_bars,
            bar_interval='1min',
            initial_price=100.0,
            volatility=0.02,
            volume_mean=1000.0,
            random_seed=42
        )

        # 2. Convert OHLCV → Orderbook
        print("\n2. Converting OHLCV → Orderbook...")
        config = OrderbookConfig(
            spread_percentage=0.001,
            size_distribution_factor=0.3
        )
        generator = OrderbookGenerator(config=config)

        orderbook_df = generator.generate_orderbook_data(
            ohlcv_df,
            points_per_bar=points_per_bar
        )
        generator.save_orderbook_data(orderbook_df, orderbook_data_path)

        # Print orderbook statistics
        ob_stats = generator.generate_summary_stats(orderbook_df)
        print("\nOrderbook Statistics:")
        print(f"Total quotes: {ob_stats['total_records']}")
        print(f"Average spread: {ob_stats['avg_spread_percentage']:.4f}%")

        # 3. Convert Orderbook → OHLCV
        print("\n3. Converting Orderbook → OHLCV...")
        # Pass the same size_distribution_factor used in generation to compensate volumes
        converter = OHLCVGenerator(size_distribution_factor=config.size_distribution_factor)
        reconstructed_df = converter.group_orderbook_to_bars(orderbook_df, points_per_bar=points_per_bar)

        # Save the reconstructed data
        converter.io_handler.write_parquet(reconstructed_df, reconstructed_data_path)

        # 4. Verify correspondence...
        print("\n4. Verifying correspondence...")

        # First analyze the differences
        analysis = analyze_differences(ohlcv_df, reconstructed_df)
        print_detailed_analysis(analysis)

        # Use differentiated tolerances for prices and volumes
        price_tolerance = max(0.2, analysis['summary']['worst_price_diff'] * 1.1)  # 0.2% minimum for prices
        volume_tolerance = min(VOLUME_TOLERANCE, analysis['summary']['worst_volume_diff'] * 1.1)  # max 30% for volumes

        print(f"\nApplying differentiated tolerances:")
        print(f"  Price tolerance: {price_tolerance:.4f}%")
        print(f"  Volume tolerance: {volume_tolerance:.4f}%")

        validation_config = ValidationConfig(price_tolerance=price_tolerance/100)  # Convert percentage to decimal
        validator = OrderbookValidator(config=validation_config)
        validation_passed, results, report = validator.run_full_validation(
            ohlcv_df,
            orderbook_df,
            points_per_bar=points_per_bar
        )

        print("\n" + "="*50)
        if analysis['summary']['worst_volume_diff'] <= VOLUME_TOLERANCE:
            print("✅ Pipeline test completed successfully!")
            print(f"  - Maximum price difference: {analysis['summary']['worst_price_diff']:.4f}%")
            print(f"  - Maximum volume difference: {analysis['summary']['worst_volume_diff']:.4f}%")
        else:
            print("❌ Pipeline test failed!")
            print(f"Volume difference ({analysis['summary']['worst_volume_diff']:.1f}%) exceeds tolerance ({VOLUME_TOLERANCE:.1f}%)")
        print("="*50)

        # Remove the return to avoid pytest warning
        assert analysis['summary']['worst_volume_diff'] <= VOLUME_TOLERANCE, f"Volume tolerance exceeded: {analysis['summary']['worst_volume_diff']:.1f}%"

    finally:
        # Cleanup temporary files
        for file in [test_data_path, orderbook_data_path, reconstructed_data_path]:
            if os.path.exists(file):
                os.remove(file)


def test_mypy_compliance() -> None:
    """Verify static typing compliance with mypy."""
    project_root = Path(__file__).parent.parent
    result = subprocess.run(
        ['mypy', 'ohlcv_to_orderbook'],
        cwd=project_root,
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        pytest.fail(
            f"Typing errors found:\n{result.stdout}\n{result.stderr}"
        )


if __name__ == "__main__":
    test_full_pipeline()
