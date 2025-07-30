"""Test conversion functions."""
import os
from datetime import datetime, timedelta
from typing import Generator

import numpy as np
import pandas as pd
import pytest

from ohlcv_to_orderbook.config import OrderbookConfig
from ohlcv_to_orderbook.ohlcv_to_orderbook import OrderbookGenerator
from ohlcv_to_orderbook.synthetic_data import generate_test_data
from ohlcv_to_orderbook.orderbook_to_ohlcv import OHLCVGenerator


@pytest.fixture
def test_data() -> Generator[pd.DataFrame, None, None]:
    """Fixture that generates test OHLCV data"""
    num_bars = 100
    df, stats = generate_test_data(
        output_file='temp_test.parquet',
        num_bars=num_bars,
        bar_interval='1min',
        initial_price=100.0,
        volatility=0.02,
        volume_mean=1000.0,
        random_seed=42
    )
    yield df
    # Cleanup
    if os.path.exists('temp_test.parquet'):
        os.remove('temp_test.parquet')


@pytest.fixture
def generator() -> OrderbookGenerator:
    """Fixture for OrderbookGenerator"""
    config = OrderbookConfig(
        spread_percentage=0.001,
        size_distribution_factor=0.3
    )
    return OrderbookGenerator(config=config)


@pytest.fixture
def converter() -> OHLCVGenerator:
    """Fixture for OHLCVGenerator"""
    # Use the same size_distribution_factor as the generator for precise reconstruction
    return OHLCVGenerator(size_distribution_factor=0.3)


def test_price_path_estimation(generator: OrderbookGenerator, test_data: pd.DataFrame) -> None:
    """Test price path estimation"""
    # Take the first bar from test data
    row = test_data.iloc[0]
    path = generator.estimate_price_path(
        float(row['open']),
        float(row['high']),
        float(row['low']),
        float(row['close'])
    )

    assert len(path) == 4, "Path must contain 4 points"
    assert path[0] == row['open'], "First point must be Open"
    assert path[-1] == row['close'], "Last point must be Close"
    assert max(path) == row['high'], "Maximum must be High"
    assert min(path) == row['low'], "Minimum must be Low"


def test_volume_distribution(generator: OrderbookGenerator, test_data: pd.DataFrame) -> None:
    """Test volume distribution"""
    row = test_data.iloc[0]
    orderbook_df = generator.generate_orderbook_data(
        pd.DataFrame([row]).reset_index(),
        points_per_bar=4
    )

    # Verify that volumes are distributed correctly
    total_volume = orderbook_df['bid_size'].sum() + orderbook_df['ask_size'].sum()
    # The total volume should be the original volume multiplied by the distribution factor
    # (not multiplied by the number of points, because it's already distributed among the points)
    expected_volume = row['volume'] * generator.config.size_distribution_factor

    # Use percentage tolerance instead of absolute decimals to handle dynamic variations
    percentage_diff = abs(total_volume - expected_volume) / expected_volume * 100
    assert percentage_diff < 1.0, f"Volume difference {percentage_diff:.2f}% exceeds 1% tolerance"


def test_spread_calculation(generator: OrderbookGenerator, test_data: pd.DataFrame) -> None:
    """Test spread calculation"""
    row = test_data.iloc[0]
    orderbook_df = generator.generate_orderbook_data(
        pd.DataFrame([row]).reset_index(),
        points_per_bar=4
    )

    # Verify that spreads are reasonable
    spreads = orderbook_df['ask_price'] - orderbook_df['bid_price']
    avg_spread_pct = (spreads / orderbook_df['mid_price']).mean() * 100

    assert avg_spread_pct >= 0.05, "Spread too narrow"
    assert avg_spread_pct <= 0.5, "Spread too wide"
    assert (spreads >= 0).all(), "Negative spread detected"


def test_full_conversion_cycle(generator: OrderbookGenerator, converter: OHLCVGenerator, test_data: pd.DataFrame) -> None:
    """Test complete conversion cycle"""
    # OHLCV → Orderbook
    orderbook_df = generator.generate_orderbook_data(test_data, points_per_bar=4)

    # Orderbook → OHLCV
    reconstructed_df = converter.group_orderbook_to_bars(orderbook_df)

    # Verify dimensions
    assert len(reconstructed_df) == len(test_data), "Number of bars does not match"

    # Verify prices with 0.2% tolerance
    for col in ['open', 'high', 'low', 'close']:
        pd.testing.assert_series_equal(
            test_data[col],
            reconstructed_df[col],
            rtol=0.002,
            check_names=False,
            check_dtype=False
        )

    # Verify volumes with 10% tolerance (drastically reduced thanks to compensation)
    pd.testing.assert_series_equal(
        test_data['volume'],
        reconstructed_df['volume'],
        rtol=0.1,  # Reduced from 70% to 10% thanks to size_distribution_factor compensation
        check_names=False,
        check_dtype=False
    )


def test_timestamp_preservation(generator: OrderbookGenerator, converter: OHLCVGenerator, test_data: pd.DataFrame) -> None:
    """Test timestamp preservation"""
    # OHLCV → Orderbook
    orderbook_df = generator.generate_orderbook_data(test_data, points_per_bar=4)

    # Verify that timestamps are incremental
    timestamps = pd.to_datetime(orderbook_df['timestamp'])
    assert (timestamps.diff()[1:] > timedelta(0)).all(), "Non-incremental timestamps"

    # Orderbook → OHLCV
    reconstructed_df = converter.group_orderbook_to_bars(orderbook_df)

    # Verify that the number of bars is correct
    assert len(reconstructed_df) == len(test_data), "Number of bars does not match"

    # Verify that time intervals are similar (not necessarily identical)
    original_interval = test_data['timestamp'].iloc[1] - test_data['timestamp'].iloc[0]
    reconstructed_interval = reconstructed_df['timestamp'].iloc[1] - reconstructed_df['timestamp'].iloc[0]

    # Verify that the interval is approximately 1 minute (allowing tolerance)
    assert abs(reconstructed_interval.total_seconds() - 60) < 5, "Incorrect time interval"


def test_edge_cases(generator: OrderbookGenerator, converter: OHLCVGenerator) -> None:
    """Test edge cases"""
    # Case 1: Constant price (O=H=L=C)
    constant_price_df = pd.DataFrame({
        'timestamp': [pd.Timestamp.now()],
        'open': [100.0],
        'high': [100.0],
        'low': [100.0],
        'close': [100.0],
        'volume': [1000.0]
    })

    orderbook_df = generator.generate_orderbook_data(constant_price_df, points_per_bar=4)
    assert len(orderbook_df) == 4, "Incorrect number of quotes for constant price"

    # Case 2: Zero volume
    zero_volume_df = pd.DataFrame({
        'timestamp': [pd.Timestamp.now()],
        'open': [100.0],
        'high': [101.0],
        'low': [99.0],
        'close': [100.5],
        'volume': [0.0]
    })

    orderbook_df = generator.generate_orderbook_data(zero_volume_df, points_per_bar=4)
    assert (orderbook_df['bid_size'] >= 0).all(), "Negative bid volumes"
    assert (orderbook_df['ask_size'] >= 0).all(), "Negative ask volumes"

    # Case 3: High volatility
    high_volatility_df = pd.DataFrame({
        'timestamp': [pd.Timestamp.now()],
        'open': [100.0],
        'high': [150.0],
        'low': [50.0],
        'close': [120.0],
        'volume': [1000.0]
    })

    orderbook_df = generator.generate_orderbook_data(high_volatility_df, points_per_bar=4)
    spreads = orderbook_df['ask_price'] - orderbook_df['bid_price']
    assert (spreads > 0).all(), "Negative spreads with high volatility"


if __name__ == '__main__':
    pytest.main([__file__])
