"""
Command Line Interface for OHLCV to Orderbook conversion.
"""
import argparse
import sys
from pathlib import Path
from typing import Optional, List

from .config import OrderbookConfig
from .data_types import ValidationConfig
from .ohlcv_to_orderbook import OrderbookGenerator, OrderbookValidator
from .orderbook_to_ohlcv import OHLCVGenerator
from .io_handlers import ParquetHandler
from .exceptions import ValidationError, ConversionError


class CLIRunner:
    """Command line interface runner for OHLCV-Orderbook conversions."""

    def __init__(self) -> None:
        self.parquet_handler = ParquetHandler()

    def create_parser(self) -> argparse.ArgumentParser:
        """Create the argument parser for the CLI."""
        parser = argparse.ArgumentParser(
            description="Convert between OHLCV and Orderbook L1 data formats",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
Examples:
  # Convert OHLCV to Orderbook
  ohlcv-converter ohlcv-to-orderbook input.parquet output.parquet
  
  # Convert Orderbook to OHLCV with custom spread
  ohlcv-converter orderbook-to-ohlcv --spread 0.002 input.parquet output.parquet
  
  # Convert with validation
  ohlcv-converter ohlcv-to-orderbook --validate input.parquet output.parquet
            """
        )

        # Subcommands
        subparsers = parser.add_subparsers(dest='command', help='Available commands')

        # OHLCV to Orderbook command
        ohlcv_parser = subparsers.add_parser(
            'ohlcv-to-orderbook',
            help='Convert OHLCV data to Orderbook L1'
        )
        self._add_ohlcv_to_orderbook_args(ohlcv_parser)

        # Orderbook to OHLCV command
        orderbook_parser = subparsers.add_parser(
            'orderbook-to-ohlcv',
            help='Convert Orderbook L1 data to OHLCV'
        )
        self._add_orderbook_to_ohlcv_args(orderbook_parser)

        # Common arguments
        parser.add_argument(
            '--verbose', '-v',
            action='store_true',
            help='Enable verbose output'
        )

        return parser

    def _add_ohlcv_to_orderbook_args(self, parser: argparse.ArgumentParser) -> None:
        """Add arguments for OHLCV to Orderbook conversion."""
        parser.add_argument(
            'input_file',
            type=str,
            help='Input OHLCV parquet file'
        )
        parser.add_argument(
            'output_file',
            type=str,
            help='Output Orderbook parquet file'
        )
        parser.add_argument(
            '--spread', '-s',
            type=float,
            default=0.001,
            help='Spread percentage (default: 0.001 = 0.1%%)'
        )
        parser.add_argument(
            '--points', '-p',
            type=int,
            default=4,
            help='Number of orderbook points per OHLCV bar (default: 4)'
        )
        parser.add_argument(
            '--size-factor', '-f',
            type=float,
            default=0.3,
            help='Volume distribution factor (default: 0.3)'
        )
        parser.add_argument(
            '--price-decimals',
            type=int,
            default=8,
            help='Decimal places for prices (default: 8)'
        )
        parser.add_argument(
            '--volume-decimals',
            type=int,
            default=8,
            help='Decimal places for volumes (default: 8)'
        )
        parser.add_argument(
            '--validate',
            action='store_true',
            help='Validate the conversion result'
        )
        parser.add_argument(
            '--verbose', '-v',
            action='store_true',
            help='Enable verbose output'
        )

    def _add_orderbook_to_ohlcv_args(self, parser: argparse.ArgumentParser) -> None:
        """Add arguments for Orderbook to OHLCV conversion."""
        parser.add_argument(
            'input_file',
            type=str,
            help='Input Orderbook parquet file'
        )
        parser.add_argument(
            'output_file',
            type=str,
            help='Output OHLCV parquet file'
        )
        parser.add_argument(
            '--validate',
            action='store_true',
            help='Validate the conversion result'
        )
        parser.add_argument(
            '--verbose', '-v',
            action='store_true',
            help='Enable verbose output'
        )

    def run_ohlcv_to_orderbook(self, args: argparse.Namespace) -> None:
        """Execute OHLCV to Orderbook conversion."""
        input_path = Path(args.input_file)
        output_path = Path(args.output_file)

        if not input_path.exists():
            print(f"Error: Input file '{input_path}' does not exist")
            sys.exit(1)

        if args.verbose:
            print(f"Loading OHLCV data from: {input_path}")

        try:
            # Load OHLCV data
            ohlcv_data = self.parquet_handler.read_ohlcv(input_path)

            if args.verbose:
                print(f"Loaded {len(ohlcv_data)} OHLCV records")
                print(f"Date range: {ohlcv_data['timestamp'].min()} to {ohlcv_data['timestamp'].max()}")

            # Configure orderbook generation
            config = OrderbookConfig(
                spread_percentage=args.spread,
                size_distribution_factor=args.size_factor,
                points_per_bar=args.points,
                price_decimals=args.price_decimals,
                volume_decimals=args.volume_decimals
            )

            # Generate orderbook
            generator = OrderbookGenerator(config)
            orderbook_data = generator.generate_orderbook(ohlcv_data)

            if args.verbose:
                print(f"Generated {len(orderbook_data)} orderbook records")

            # Validate if requested
            if args.validate:
                if args.verbose:
                    print("Validating conversion...")

                validator = OrderbookValidator(ValidationConfig())
                validation_result = validator.validate_conversion(ohlcv_data, orderbook_data)

                if validation_result.is_valid:
                    if args.verbose:
                        print("✓ Validation passed")
                else:
                    print("⚠ Validation warnings:")
                    for warning in validation_result.warnings:
                        print(f"  - {warning}")

                    if validation_result.errors:
                        print("✗ Validation errors:")
                        for error in validation_result.errors:
                            print(f"  - {error}")
                        sys.exit(1)

            # Save result
            if args.verbose:
                print(f"Saving orderbook data to: {output_path}")

            self.parquet_handler.write_orderbook(orderbook_data, output_path)

            if args.verbose:
                print("✓ Conversion completed successfully")

        except (ValidationError, ConversionError) as e:
            print(f"Error: {e}")
            sys.exit(1)
        except Exception as e:
            print(f"Unexpected error: {e}")
            sys.exit(1)

    def run_orderbook_to_ohlcv(self, args: argparse.Namespace) -> None:
        """Execute Orderbook to OHLCV conversion."""
        input_path = Path(args.input_file)
        output_path = Path(args.output_file)

        if not input_path.exists():
            print(f"Error: Input file '{input_path}' does not exist")
            sys.exit(1)

        if args.verbose:
            print(f"Loading Orderbook data from: {input_path}")

        try:
            # Load orderbook data
            orderbook_data = self.parquet_handler.read_orderbook(input_path)

            if args.verbose:
                print(f"Loaded {len(orderbook_data)} orderbook records")
                print(f"Date range: {orderbook_data['timestamp'].min()} to {orderbook_data['timestamp'].max()}")

            # Generate OHLCV
            generator = OHLCVGenerator()
            ohlcv_data = generator.generate_ohlcv(orderbook_data)

            if args.verbose:
                print(f"Generated {len(ohlcv_data)} OHLCV records")

            # Validate if requested
            if args.validate:
                if args.verbose:
                    print("Validating conversion...")

                validator = OrderbookValidator(ValidationConfig())
                # Re-generate orderbook for validation
                config = OrderbookConfig()
                orderbook_generator = OrderbookGenerator(config)
                regenerated_orderbook = orderbook_generator.generate_orderbook(ohlcv_data)

                validation_result = validator.validate_conversion(ohlcv_data, regenerated_orderbook)

                if validation_result.is_valid:
                    if args.verbose:
                        print("✓ Validation passed")
                else:
                    print("⚠ Validation warnings:")
                    for warning in validation_result.warnings:
                        print(f"  - {warning}")

                    if validation_result.errors:
                        print("✗ Validation errors:")
                        for error in validation_result.errors:
                            print(f"  - {error}")
                        sys.exit(1)

            # Save result
            if args.verbose:
                print(f"Saving OHLCV data to: {output_path}")

            self.parquet_handler.write_ohlcv(ohlcv_data, output_path)

            if args.verbose:
                print("✓ Conversion completed successfully")

        except (ValidationError, ConversionError) as e:
            print(f"Error: {e}")
            sys.exit(1)
        except Exception as e:
            print(f"Unexpected error: {e}")
            sys.exit(1)

    def run(self, args: Optional[List[str]] = None) -> None:
        """Run the CLI with the given arguments."""
        parser = self.create_parser()
        parsed_args = parser.parse_args(args)

        if not parsed_args.command:
            parser.print_help()
            sys.exit(1)

        if parsed_args.command == 'ohlcv-to-orderbook':
            self.run_ohlcv_to_orderbook(parsed_args)
        elif parsed_args.command == 'orderbook-to-ohlcv':
            self.run_orderbook_to_ohlcv(parsed_args)


def main() -> None:
    """Main entry point for the CLI."""
    cli = CLIRunner()
    cli.run()


if __name__ == '__main__':
    main()
