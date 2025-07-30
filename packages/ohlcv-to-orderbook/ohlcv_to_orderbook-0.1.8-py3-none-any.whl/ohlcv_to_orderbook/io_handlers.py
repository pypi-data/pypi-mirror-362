"""
I/O handling for Parquet files with data validation.
"""
import logging
from pathlib import Path
from typing import Union, Optional, Dict, Any, List
from datetime import datetime

import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

from .config import IOConfig
from .exceptions import ValidationError, IOError

logger = logging.getLogger(__name__)


class ParquetHandler:
    """Handler for reading/writing Parquet files with validation."""

    def __init__(self, config: Optional[IOConfig] = None):
        """
        Initialize the I/O handler.

        Args:
            config: Optional I/O configuration
        """
        self.config = config or IOConfig()
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

    def read_parquet(
        self,
        file_path: Union[str, Path],
        columns: Optional[List[str]] = None
    ) -> pd.DataFrame:
        """
        Read a Parquet file with validation.

        Args:
            file_path: File path
            columns: Optional list of columns to read

        Returns:
            DataFrame with data

        Raises:
            IOError: If there are reading problems
        """
        try:
            file_path = Path(file_path)
            if not file_path.exists():
                raise IOError(f"File not found: {file_path}")

            logger.info(f"Reading file: {file_path}")
            df = pd.read_parquet(file_path, columns=columns)

            if df.empty:
                raise IOError("File contains no data")

            logger.info(f"Read {len(df)} records from {file_path}")
            return df

        except Exception as e:
            raise IOError(f"Error reading file {file_path}: {e}") from e

    def write_parquet(
        self,
        df: pd.DataFrame,
        file_path: Union[str, Path],
        schema: Optional[pa.Schema] = None
    ) -> None:
        """
        Write a DataFrame to Parquet format.

        Args:
            df: DataFrame to save
            file_path: File path
            schema: Optional PyArrow schema

        Raises:
            IOError: If there are writing problems
        """
        try:
            file_path = Path(file_path)
            file_path.parent.mkdir(parents=True, exist_ok=True)

            logger.info(f"Writing {len(df)} records to {file_path}")

            table = pa.Table.from_pandas(df, schema=schema)

            pq.write_table(
                table,
                file_path,
                compression=self.config.compression,
                row_group_size=self.config.row_group_size
            )

            logger.info(f"Successfully wrote file: {file_path}")

        except Exception as e:
            raise IOError(f"Error writing file {file_path}: {e}") from e

    def validate_schema(
        self,
        df: pd.DataFrame,
        expected_columns: List[str],
        column_types: Optional[Dict[str, str]] = None
    ) -> None:
        """
        Validate DataFrame schema.

        Args:
            df: DataFrame to validate
            expected_columns: List of expected columns
            column_types: Optional dictionary of expected column types

        Raises:
            ValidationError: If schema validation fails
        """
        missing_columns = set(expected_columns) - set(df.columns)
        if missing_columns:
            raise ValidationError(f"Missing columns: {missing_columns}")

        if column_types:
            for col, expected_type in column_types.items():
                if col in df.columns:
                    actual_type = str(df[col].dtype)
                    if expected_type not in actual_type:
                        raise ValidationError(
                            f"Column {col} has type {actual_type}, expected {expected_type}"
                        )

    def get_file_info(self, file_path: Union[str, Path]) -> Dict[str, Any]:
        """
        Get information about a Parquet file.

        Args:
            file_path: File path

        Returns:
            Dictionary with file information
        """
        try:
            file_path = Path(file_path)
            if not file_path.exists():
                raise IOError(f"File not found: {file_path}")

            parquet_file = pq.ParquetFile(file_path)
            metadata = parquet_file.metadata

            return {
                'num_rows': metadata.num_rows,
                'num_columns': metadata.num_columns,
                'size_bytes': file_path.stat().st_size,
                'created': datetime.fromtimestamp(file_path.stat().st_ctime),
                'modified': datetime.fromtimestamp(file_path.stat().st_mtime),
                'schema': parquet_file.schema.to_arrow_schema()
            }

        except Exception as e:
            raise IOError(f"Error getting file info {file_path}: {e}") from e

    def read_ohlcv(self, file_path: Union[str, Path]) -> pd.DataFrame:
        """
        Read OHLCV data from a Parquet file.

        Args:
            file_path: File path

        Returns:
            DataFrame with OHLCV data

        Raises:
            IOError: If there are reading problems
            ValidationError: If data validation fails
        """
        df = self.read_parquet(file_path)

        # Validate OHLCV schema
        expected_columns = ['timestamp', 'open', 'high', 'low', 'close', 'volume']
        self.validate_schema(df, expected_columns)

        return df

    def write_ohlcv(self, df: pd.DataFrame, file_path: Union[str, Path]) -> None:
        """
        Write OHLCV data to a Parquet file.

        Args:
            df: DataFrame with OHLCV data
            file_path: File path

        Raises:
            IOError: If there are writing problems
            ValidationError: If data validation fails
        """
        # Validate OHLCV schema
        expected_columns = ['timestamp', 'open', 'high', 'low', 'close', 'volume']
        self.validate_schema(df, expected_columns)

        self.write_parquet(df, file_path)

    def read_orderbook(self, file_path: Union[str, Path]) -> pd.DataFrame:
        """
        Read orderbook data from a Parquet file.

        Args:
            file_path: File path

        Returns:
            DataFrame with orderbook data

        Raises:
            IOError: If there are reading problems
            ValidationError: If data validation fails
        """
        df = self.read_parquet(file_path)

        # Validate orderbook schema
        expected_columns = ['timestamp', 'bid_price', 'bid_size', 'ask_price', 'ask_size']
        self.validate_schema(df, expected_columns)

        return df

    def write_orderbook(self, df: pd.DataFrame, file_path: Union[str, Path]) -> None:
        """
        Write orderbook data to a Parquet file.

        Args:
            df: DataFrame with orderbook data
            file_path: File path

        Raises:
            IOError: If there are writing problems
            ValidationError: If data validation fails
        """
        # Validate orderbook schema
        expected_columns = ['timestamp', 'bid_price', 'bid_size', 'ask_price', 'ask_size']
        self.validate_schema(df, expected_columns)

        self.write_parquet(df, file_path)
