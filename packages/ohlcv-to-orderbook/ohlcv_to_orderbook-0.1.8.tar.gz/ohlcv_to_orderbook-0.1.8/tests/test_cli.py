"""
Tests for the CLI module.
"""
import pytest
import tempfile
import pandas as pd
from pathlib import Path
from unittest.mock import patch
import sys

from ohlcv_to_orderbook.cli import CLIRunner
from ohlcv_to_orderbook.synthetic_data import generate_test_data


class TestCLIRunner:
    """Test cases for the CLI runner."""

    def setup_method(self):
        """Set up test fixtures."""
        self.cli = CLIRunner()

        # Generate test data
        with tempfile.NamedTemporaryFile(suffix='.parquet', delete=False) as tmp:
            self.test_ohlcv, _ = generate_test_data(
                output_file=tmp.name,
                num_bars=10,
                initial_price=50000.0
            )

        # Generate test orderbook data from OHLCV
        from ohlcv_to_orderbook.ohlcv_to_orderbook import OrderbookGenerator
        from ohlcv_to_orderbook.config import OrderbookConfig

        generator = OrderbookGenerator(OrderbookConfig())
        self.test_orderbook = generator.generate_orderbook(self.test_ohlcv)

    def test_create_parser(self):
        """Test parser creation."""
        parser = self.cli.create_parser()

        assert parser is not None
        assert parser.prog is not None

        # Test help doesn't crash
        with pytest.raises(SystemExit):
            parser.parse_args(['--help'])

    def test_ohlcv_to_orderbook_args(self):
        """Test OHLCV to orderbook argument parsing."""
        parser = self.cli.create_parser()

        args = parser.parse_args([
            'ohlcv-to-orderbook',
            'input.parquet',
            'output.parquet',
            '--spread', '0.002',
            '--points', '6',
            '--validate',
            '--verbose'
        ])

        assert args.command == 'ohlcv-to-orderbook'
        assert args.input_file == 'input.parquet'
        assert args.output_file == 'output.parquet'
        assert args.spread == 0.002
        assert args.points == 6
        assert args.validate is True
        assert args.verbose is True

    def test_orderbook_to_ohlcv_args(self):
        """Test orderbook to OHLCV argument parsing."""
        parser = self.cli.create_parser()

        args = parser.parse_args([
            'orderbook-to-ohlcv',
            'input.parquet',
            'output.parquet',
            '--validate',
            '--verbose'
        ])

        assert args.command == 'orderbook-to-ohlcv'
        assert args.input_file == 'input.parquet'
        assert args.output_file == 'output.parquet'
        assert args.validate is True
        assert args.verbose is True

    def test_ohlcv_to_orderbook_conversion(self):
        """Test complete OHLCV to orderbook conversion via CLI."""
        with tempfile.TemporaryDirectory() as temp_dir:
            input_file = Path(temp_dir) / "input_ohlcv.parquet"
            output_file = Path(temp_dir) / "output_orderbook.parquet"

            # Save test OHLCV data
            self.cli.parquet_handler.write_ohlcv(self.test_ohlcv, input_file)

            # Test CLI conversion
            args = [
                'ohlcv-to-orderbook',
                str(input_file),
                str(output_file),
                '--spread', '0.001',
                '--points', '4',
                '--verbose'
            ]

            # Capture stdout
            with patch('sys.stdout.write') as mock_stdout:
                self.cli.run(args)

            # Verify output file exists
            assert output_file.exists()

            # Verify output data
            result_orderbook = self.cli.parquet_handler.read_orderbook(output_file)
            assert len(result_orderbook) > 0
            assert 'timestamp' in result_orderbook.columns
            assert 'bid_price' in result_orderbook.columns
            assert 'ask_price' in result_orderbook.columns

    def test_orderbook_to_ohlcv_conversion(self):
        """Test complete orderbook to OHLCV conversion via CLI."""
        with tempfile.TemporaryDirectory() as temp_dir:
            input_file = Path(temp_dir) / "input_orderbook.parquet"
            output_file = Path(temp_dir) / "output_ohlcv.parquet"

            # Save test orderbook data
            self.cli.parquet_handler.write_orderbook(self.test_orderbook, input_file)

            # Test CLI conversion
            args = [
                'orderbook-to-ohlcv',
                str(input_file),
                str(output_file),
                '--verbose'
            ]

            # Capture stdout
            with patch('sys.stdout.write') as mock_stdout:
                self.cli.run(args)

            # Verify output file exists
            assert output_file.exists()

            # Verify output data
            result_ohlcv = self.cli.parquet_handler.read_ohlcv(output_file)
            assert len(result_ohlcv) > 0
            assert 'timestamp' in result_ohlcv.columns
            assert 'open' in result_ohlcv.columns
            assert 'high' in result_ohlcv.columns
            assert 'low' in result_ohlcv.columns
            assert 'close' in result_ohlcv.columns
            assert 'volume' in result_ohlcv.columns

    def test_input_file_not_found(self):
        """Test error handling when input file doesn't exist."""
        with tempfile.TemporaryDirectory() as temp_dir:
            input_file = Path(temp_dir) / "nonexistent.parquet"
            output_file = Path(temp_dir) / "output.parquet"

            args = [
                'ohlcv-to-orderbook',
                str(input_file),
                str(output_file)
            ]

            with pytest.raises(SystemExit) as exc_info:
                self.cli.run(args)

            assert exc_info.value.code == 1

    def test_validation_with_cli(self):
        """Test validation option in CLI."""
        with tempfile.TemporaryDirectory() as temp_dir:
            input_file = Path(temp_dir) / "input_ohlcv.parquet"
            output_file = Path(temp_dir) / "output_orderbook.parquet"

            # Save test OHLCV data
            self.cli.parquet_handler.write_ohlcv(self.test_ohlcv, input_file)

            # Test CLI conversion with validation
            args = [
                'ohlcv-to-orderbook',
                str(input_file),
                str(output_file),
                '--validate',
                '--verbose'
            ]

            # Should not raise an exception
            self.cli.run(args)

            # Verify output file exists
            assert output_file.exists()

    def test_no_command_shows_help(self):
        """Test that running without command shows help."""
        with pytest.raises(SystemExit) as exc_info:
            self.cli.run([])

        assert exc_info.value.code == 1

    def test_custom_configuration_parameters(self):
        """Test CLI with custom configuration parameters."""
        with tempfile.TemporaryDirectory() as temp_dir:
            input_file = Path(temp_dir) / "input_ohlcv.parquet"
            output_file = Path(temp_dir) / "output_orderbook.parquet"

            # Save test OHLCV data
            self.cli.parquet_handler.write_ohlcv(self.test_ohlcv, input_file)

            # Test CLI conversion with custom parameters
            args = [
                'ohlcv-to-orderbook',
                str(input_file),
                str(output_file),
                '--spread', '0.005',
                '--points', '8',
                '--size-factor', '0.5',
                '--price-decimals', '6',
                '--volume-decimals', '4',
                '--verbose'
            ]

            self.cli.run(args)

            # Verify output file exists
            assert output_file.exists()

            # Verify output data has expected characteristics
            result_orderbook = self.cli.parquet_handler.read_orderbook(output_file)
            assert len(result_orderbook) > 0

            # Check that we have the expected number of points per bar
            # (Should be 8 points per original OHLCV bar)
            expected_points = len(self.test_ohlcv) * 8
            assert len(result_orderbook) == expected_points


class TestCLIIntegration:
    """Integration tests for the CLI."""

    def test_main_function_exists(self):
        """Test that main function exists and is callable."""
        from ohlcv_to_orderbook.cli import main

        # Test that main function exists
        assert callable(main)

        # Test that it handles no arguments gracefully
        with pytest.raises(SystemExit):
            main()

    def test_round_trip_conversion(self):
        """Test complete round-trip conversion via CLI."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Generate test data
            test_file = Path(temp_dir) / "test_data.parquet"
            original_ohlcv, _ = generate_test_data(
                output_file=str(test_file),
                num_bars=5,
                initial_price=3000.0
            )

            # File paths
            ohlcv_file = Path(temp_dir) / "original.parquet"
            orderbook_file = Path(temp_dir) / "orderbook.parquet"
            roundtrip_ohlcv_file = Path(temp_dir) / "roundtrip.parquet"

            # Save original OHLCV
            cli = CLIRunner()
            cli.parquet_handler.write_ohlcv(original_ohlcv, ohlcv_file)

            # Convert OHLCV to orderbook
            cli.run([
                'ohlcv-to-orderbook',
                str(ohlcv_file),
                str(orderbook_file),
                '--spread', '0.001'
            ])

            # Convert orderbook back to OHLCV
            cli.run([
                'orderbook-to-ohlcv',
                str(orderbook_file),
                str(roundtrip_ohlcv_file)
            ])

            # Verify all files exist
            assert ohlcv_file.exists()
            assert orderbook_file.exists()
            assert roundtrip_ohlcv_file.exists()

            # Load and compare data
            roundtrip_ohlcv = cli.parquet_handler.read_ohlcv(roundtrip_ohlcv_file)

            # Basic structure checks
            assert len(roundtrip_ohlcv) == len(original_ohlcv)
            assert list(roundtrip_ohlcv.columns) == list(original_ohlcv.columns)
