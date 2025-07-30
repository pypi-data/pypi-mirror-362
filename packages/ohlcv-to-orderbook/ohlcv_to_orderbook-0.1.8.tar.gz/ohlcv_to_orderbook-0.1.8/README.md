# OHLCV to Orderbook Converter

[![PyPI version](https://badge.fury.io/py/ohlcv-to-orderbook.svg)](https://badge.fury.io/py/ohlcv-to-orderbook)
[![Python](https://img.shields.io/pypi/pyversions/ohlcv-to-orderbook.svg)](https://pypi.org/project/ohlcv-to-orderbook/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Build Status](https://github.com/obseries/ohlcv-to-orderbook/workflows/CI/badge.svg)](https://github.com/obseries/ohlcv-to-orderbook/actions)
[![Coverage Status](https://codecov.io/gh/obseries/ohlcv-to-orderbook/branch/main/graph/badge.svg)](https://codecov.io/gh/obseries/ohlcv-to-orderbook)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A Python library for converting OHLCV (Open, High, Low, Close, Volume) data to synthetic Level 1 orderbook representation and vice versa, designed for financial data processing and validation.

## Overview

This project provides a bidirectional conversion pipeline between OHLCV bars and synthetic orderbook snapshots. The conversion maintains data integrity and allows for round-trip validation, making it useful for:

- Financial data preprocessing
- Trading algorithm testing
- Market data validation
- Quantitative research

## Features

- **Bidirectional Conversion**: Convert OHLCV data to orderbook snapshots and back
- **Synthetic Orderbook Generation**: Creates realistic Level 1 orderbook data from OHLCV bars
- **Parquet I/O Support**: Efficient reading and writing of financial data using Apache Parquet
- **Data Validation**: Built-in validation for data integrity and consistency
- **Type Safety**: Full type annotations and mypy compatibility
- **Configurable Parameters**: Customizable spread generation and price path estimation
- **Comprehensive Testing**: Full test coverage with round-trip validation

## Installation

### From PyPI (Recommended)

```bash
pip install ohlcv-to-orderbook
```

### From PyPI with development dependencies

```bash
pip install "ohlcv-to-orderbook[dev]"
```

### Prerequisites

- Python 3.8 or higher
- pip or uv package manager

### Install from source

```bash
git clone https://github.com/luca/ohlcv-to-orderbook.git
cd ohlcv-to-orderbook
pip install -e .
```

### Development installation

```bash
git clone https://github.com/luca/ohlcv-to-orderbook.git
cd ohlcv-to-orderbook
pip install -e ".[dev]"
```

## Quick Start

### Basic Usage

```python
from ohlcv_to_orderbook import OrderbookGenerator, OHLCVGenerator
import pandas as pd

# Create sample OHLCV data
ohlcv_data = pd.DataFrame({
    'timestamp': [1640995200, 1640995260, 1640995320],
    'open': [50000.0, 50100.0, 50050.0],
    'high': [50200.0, 50150.0, 50100.0],
    'low': [49900.0, 50000.0, 49950.0],
    'close': [50100.0, 50050.0, 50080.0],
    'volume': [1.5, 2.3, 1.8]
})

# Convert OHLCV to orderbook
orderbook_gen = OrderbookGenerator()
orderbook_data = orderbook_gen.generate_orderbook(ohlcv_data)

# Convert back to OHLCV
ohlcv_gen = OHLCVGenerator()
reconstructed_ohlcv = ohlcv_gen.generate_ohlcv(orderbook_data)

print("Original OHLCV:", ohlcv_data)
print("Reconstructed OHLCV:", reconstructed_ohlcv)
```

### Working with Parquet Files

```python
from ohlcv_to_orderbook import OrderbookGenerator
from ohlcv_to_orderbook.io_handlers import ParquetHandler

# Initialize components
generator = OrderbookGenerator()
io_handler = ParquetHandler()

# Read OHLCV data from Parquet
ohlcv_data = io_handler.read_ohlcv("input_data.parquet")

# Convert to orderbook
orderbook_data = generator.generate_orderbook(ohlcv_data)

# Save orderbook data
io_handler.write_orderbook(orderbook_data, "orderbook_output.parquet")
```

### Generating Synthetic Test Data

```python
from ohlcv_to_orderbook import generate_test_data

# Generate synthetic data for testing
ohlcv_data, orderbook_data = generate_test_data(
    n_bars=100,
    symbol="BTCUSD",
    start_price=50000.0
)
```

## Command Line Interface (CLI)

The package provides a powerful command-line interface for batch processing and automation.

### Installation

After installing the package, the `ohlcv-converter` command will be available:

```bash
# Install the package
pip install -e .

# The CLI command is now available
ohlcv-converter --help
```

### CLI Usage

#### Convert OHLCV to Orderbook

```bash
# Basic conversion
ohlcv-converter ohlcv-to-orderbook input_ohlcv.parquet output_orderbook.parquet

# With custom parameters
ohlcv-converter ohlcv-to-orderbook \
    --spread 0.002 \
    --points 6 \
    --size-factor 0.4 \
    --price-decimals 8 \
    --volume-decimals 6 \
    --validate \
    --verbose \
    input_ohlcv.parquet output_orderbook.parquet
```

#### Convert Orderbook to OHLCV

```bash
# Basic conversion
ohlcv-converter orderbook-to-ohlcv input_orderbook.parquet output_ohlcv.parquet

# With validation and verbose output
ohlcv-converter orderbook-to-ohlcv \
    --validate \
    --verbose \
    input_orderbook.parquet output_ohlcv.parquet
```

#### CLI Options

**OHLCV to Orderbook Options:**
- `--spread, -s`: Spread percentage (default: 0.001 = 0.1%)
- `--points, -p`: Number of orderbook points per OHLCV bar (default: 4)
- `--size-factor, -f`: Volume distribution factor (default: 0.3)
- `--price-decimals`: Decimal places for prices (default: 8)
- `--volume-decimals`: Decimal places for volumes (default: 8)
- `--validate`: Validate the conversion result
- `--verbose, -v`: Enable verbose output

**Orderbook to OHLCV Options:**
- `--validate`: Validate the conversion result
- `--verbose, -v`: Enable verbose output

#### CLI Examples

```bash
# Convert with high precision and validation
ohlcv-converter ohlcv-to-orderbook \
    --spread 0.0005 \
    --points 8 \
    --validate \
    --verbose \
    btc_ohlcv_1m.parquet btc_orderbook_l1.parquet

# Round-trip conversion test
ohlcv-converter ohlcv-to-orderbook original.parquet temp_orderbook.parquet
ohlcv-converter orderbook-to-ohlcv temp_orderbook.parquet reconstructed.parquet

# Process multiple timeframes
for file in data/ohlcv_*.parquet; do
    output="orderbook_$(basename "$file")"
    ohlcv-converter ohlcv-to-orderbook --validate "$file" "$output"
done
```

## Configuration

The library supports various configuration options:

```python
from ohlcv_to_orderbook.config import OrderbookConfig

config = OrderbookConfig(
    min_spread_bps=1.0,      # Minimum spread in basis points
    max_spread_bps=10.0,     # Maximum spread in basis points
    volume_distribution='uniform',  # Volume distribution method
    price_precision=2,       # Decimal places for prices
    volume_precision=8       # Decimal places for volumes
)

generator = OrderbookGenerator(config=config)
```

## Data Format

### OHLCV Data Format

The expected OHLCV data format is a pandas DataFrame with the following columns:

- `timestamp`: Unix timestamp (int)
- `open`: Opening price (float)
- `high`: Highest price (float)
- `low`: Lowest price (float)
- `close`: Closing price (float)
- `volume`: Volume traded (float)

### Orderbook Data Format

The generated orderbook data is a pandas DataFrame with:

- `timestamp`: Unix timestamp (int)
- `bid_price`: Best bid price (float)
- `bid_size`: Best bid volume (float)
- `ask_price`: Best ask price (float)
- `ask_size`: Best ask volume (float)

## Algorithm Details

### OHLCV to Orderbook Conversion

The conversion algorithm estimates the price path within each OHLCV bar:

1. **Path Determination**: Decides the price sequence based on the relationship between Open, High, and Low:
   - If Open is closer to High: Open → High → Low → Close
   - If Open is closer to Low: Open → Low → High → Close

2. **Spread Generation**: Creates realistic bid-ask spreads based on:
   - Market volatility (derived from High-Low range)
   - Volume patterns
   - Configurable spread parameters

3. **Volume Distribution**: Distributes the total volume across generated orderbook snapshots

### Orderbook to OHLCV Conversion

The reverse conversion aggregates orderbook snapshots:

1. **Price Aggregation**: Calculates OHLCV values from bid/ask prices over time intervals
2. **Volume Summation**: Sums volumes across all snapshots in the time period
3. **Timestamp Alignment**: Groups snapshots by time intervals

## Testing

Run the complete test suite:

```bash
# Run all tests
pytest

# Run with coverage
python run_tests_with_coverage.py

# Run specific test files
pytest tests/test_conversions.py
pytest tests/test_pipeline.py
```

### Round-trip Validation

The library includes comprehensive round-trip tests to ensure data integrity:

```python
# Example of round-trip validation
original_ohlcv = generate_test_data(num_bars=50)
orderbook_data = orderbook_gen.generate_orderbook(original_ohlcv)
reconstructed_ohlcv = ohlcv_gen.generate_ohlcv(orderbook_data)

# Validate reconstruction accuracy
assert_ohlcv_similarity(original_ohlcv, reconstructed_ohlcv, tolerance=0.01)
```

## Development

### Setting up Development Environment

```bash
git clone <repository-url>
cd ohlcv-to-orderbook
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -e ".[dev]"
```

### Code Quality

The project uses several tools for code quality:

```bash
# Type checking
mypy ohlcv_to_orderbook/

# Run tests with coverage
pytest --cov=ohlcv_to_orderbook tests/

# Format code (if using black)
black ohlcv_to_orderbook/ tests/
```

### Project Structure

```
ohlcv-to-orderbook/
├── ohlcv_to_orderbook/          # Main package
│   ├── __init__.py              # Package initialization
│   ├── config.py                # Configuration classes
│   ├── data_types.py            # Type definitions
│   ├── exceptions.py            # Custom exceptions
│   ├── io_handlers.py           # Parquet I/O operations
│   ├── ohlcv_to_orderbook.py    # OHLCV → Orderbook conversion
│   ├── orderbook_to_ohlcv.py    # Orderbook → OHLCV conversion
│   └── synthetic_data.py        # Test data generation
├── tests/                       # Test files
│   ├── test_conversions.py      # Conversion tests
│   └── test_pipeline.py         # End-to-end pipeline tests
├── pyproject.toml              # Project configuration
├── mypy.ini                    # Type checking configuration
└── README.md                   # This file
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass (`pytest`)
6. Run type checking (`mypy ohlcv_to_orderbook/`)
7. Commit your changes (`git commit -m 'Add amazing feature'`)
8. Push to the branch (`git push origin feature/amazing-feature`)
9. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Built with pandas for data manipulation
- Uses PyArrow for efficient Parquet I/O
- Type safety provided by mypy
- Testing framework: pytest

## Support

For questions, issues, or contributions, please open an issue on the project repository.
