# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Initial release preparation

## [0.1.0] - 2025-06-28

### Added
- Initial release of OHLCV to Orderbook Converter
- Bidirectional conversion between OHLCV and synthetic orderbook data
- Support for Parquet file I/O
- Comprehensive test suite with >90% coverage
- Type safety with full mypy support
- Command-line interface (CLI) for easy usage
- Configurable parameters for spread generation and precision
- Data validation and round-trip testing
- Complete documentation and examples

### Features
- `OHLCVToOrderbook` class for OHLCV to orderbook conversion
- `OrderbookToOHLCV` class for orderbook to OHLCV conversion
- `OrderbookConfig` for customizable conversion parameters
- `IOHandlers` for efficient Parquet file operations
- `SyntheticDataGenerator` for test data creation
- CLI commands: `ohlcv-converter`, `ohlcv-to-orderbook`, `orderbook-to-ohlcv`
- Comprehensive error handling and custom exceptions
- Full type annotations and mypy compatibility

### Technical
- Python 3.8+ support
- Dependencies: pandas, numpy, pyarrow
- Development tools: pytest, pytest-cov, mypy
- CI/CD ready configuration
- MIT License
