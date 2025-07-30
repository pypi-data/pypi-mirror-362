from datetime import datetime
from typing import Dict, Optional, Tuple, Any

import numpy as np
import pandas as pd


class OHLCVGenerator:
    """
    Generator for synthetic OHLCV data with realistic price movements and volume patterns.
    """

    def __init__(
        self,
        initial_price: float = 100.0,
        volatility: float = 0.02,
        trend: float = 0.0,
        volume_mean: float = 1000.0,
        volume_std: float = 200.0,
        random_seed: Optional[int] = None
    ):
        """
        Initialize the OHLCV data generator.

        Args:
            initial_price: Starting price for the series
            volatility: Daily volatility (standard deviation of returns)
            trend: Daily trend (drift) in price movement
            volume_mean: Mean volume per bar
            volume_std: Standard deviation of volume
            random_seed: Seed for reproducibility
        """
        self.initial_price = initial_price
        self.volatility = volatility
        self.trend = trend
        self.volume_mean = volume_mean
        self.volume_std = volume_std

        if random_seed is not None:
            np.random.seed(random_seed)

    def generate_price_path(
        self,
        num_bars: int,
        bar_interval: str = '1min'
    ) -> Tuple[pd.DataFrame, Dict[str, Any]]:
        """
        Generate synthetic OHLCV bars with realistic price movement.

        Args:
            num_bars: Number of bars to generate
            bar_interval: Time interval for each bar (e.g., '1min', '5min', '1h')

        Returns:
            Tuple of (DataFrame with OHLCV data, Dictionary with generation stats)
        """
        # Generate timestamps
        end_time = datetime.now().replace(microsecond=0, second=0)
        timestamps = pd.date_range(
            end=end_time,
            periods=num_bars,
            freq=bar_interval
        )

        # Generate log returns with trend and volatility
        returns = np.random.normal(
            loc=self.trend / np.sqrt(252 * 24 * 60),  # Annualized to per-minute
            scale=self.volatility / np.sqrt(252 * 24 * 60),
            size=num_bars
        )

        # Generate close prices
        close_prices = self.initial_price * np.exp(np.cumsum(returns))

        # Generate OHLC prices with realistic relationships
        data = []
        for i in range(num_bars):
            close = close_prices[i]

            # Generate high and low with realistic ranges
            high_low_range = close * self.volatility * np.random.uniform(0.2, 1.0)
            high = close + high_low_range * np.random.uniform(0.3, 0.7)
            low = close - high_low_range * np.random.uniform(0.3, 0.7)

            # Generate open with tendency to be between previous close and current close
            prev_close = close_prices[i-1] if i > 0 else self.initial_price
            open_price = np.random.uniform(
                min(prev_close, close),
                max(prev_close, close)
            )

            # Ensure OHLC relationships are valid
            open_price = max(min(open_price, high), low)

            # Generate volume with log-normal distribution
            volume = np.random.lognormal(
                mean=np.log(self.volume_mean),
                sigma=self.volume_std / self.volume_mean
            )

            # Volume tends to be higher when price moves more
            price_move = abs(close - prev_close) / prev_close
            volume *= (1 + price_move * 5)

            data.append({
                'timestamp': timestamps[i],
                'open': open_price,
                'high': high,
                'low': low,
                'close': close,
                'volume': volume
            })

        df = pd.DataFrame(data)

        # Calculate generation statistics
        stats = {
            'price_stats': {
                'initial': self.initial_price,
                'final': close_prices[-1],
                'return': (close_prices[-1] / self.initial_price - 1) * 100,
                'min': df['low'].min(),
                'max': df['high'].max(),
                'realized_volatility': np.std(returns) * np.sqrt(252 * 24 * 60)
            },
            'volume_stats': {
                'mean': df['volume'].mean(),
                'std': df['volume'].std(),
                'min': df['volume'].min(),
                'max': df['volume'].max()
            },
            'time_stats': {
                'start': timestamps[0],
                'end': timestamps[-1],
                'interval': bar_interval,
                'num_bars': num_bars
            }
        }

        return df, stats


def generate_test_data(
    output_file: str,
    num_bars: int = 1000,
    bar_interval: str = '1min',
    initial_price: float = 100.0,
    volatility: float = 0.02,
    trend: float = 0.0,
    volume_mean: float = 1000.0,
    volume_std: float = 200.0,
    random_seed: Optional[int] = None
) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """
    Generate test OHLCV data and save to file.

    Args:
        output_file: Path to save the generated data
        num_bars: Number of bars to generate
        bar_interval: Time interval for each bar
        initial_price: Starting price
        volatility: Daily volatility
        trend: Daily trend
        volume_mean: Mean volume
        volume_std: Volume standard deviation
        random_seed: Random seed for reproducibility

    Returns:
        Tuple of (Generated DataFrame, Statistics dictionary)
    """
    generator = OHLCVGenerator(
        initial_price=initial_price,
        volatility=volatility,
        trend=trend,
        volume_mean=volume_mean,
        volume_std=volume_std,
        random_seed=random_seed
    )

    df, stats = generator.generate_price_path(num_bars, bar_interval)

    # Save to file
    if output_file.endswith('.parquet'):
        df.to_parquet(output_file, index=False)
    else:
        df.to_parquet(output_file + '.parquet', index=False)

    print(f"Generated {num_bars} OHLCV bars and saved to {output_file}")
    print("\nGeneration Statistics:")
    print(f"Price movement: {stats['price_stats']['return']:.2f}%")
    print(f"Price range: {stats['price_stats']['min']:.2f} - {stats['price_stats']['max']:.2f}")
    print(f"Realized volatility: {stats['price_stats']['realized_volatility']*100:.1f}%")
    print(f"Average volume: {stats['volume_stats']['mean']:.0f}")
    print(f"Time period: {stats['time_stats']['start']} to {stats['time_stats']['end']}")

    return df, stats


def generate_synthetic_data(
    output_file: Optional[str] = None,
    num_bars: int = 100,
    bar_interval: str = '1min',
    initial_price: float = 100.0,
    volatility: float = 0.02,
    volume_mean: float = 1000.0,
    random_seed: Optional[int] = None
) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """
    Genera dati OHLCV sintetici con movimenti di prezzo realistici.

    Args:
        output_file: File dove salvare i dati generati (opzionale)
        num_bars: Numero di barre da generare
        bar_interval: Intervallo temporale delle barre (default: '1min')
        initial_price: Prezzo iniziale
        volatility: Volatilità target (deviazione standard dei rendimenti)
        volume_mean: Volume medio per barra
        random_seed: Seed per la generazione casuale

    Returns:
        Tuple con (DataFrame OHLCV, dizionario con statistiche)
    """
    if random_seed is not None:
        np.random.seed(random_seed)

    # Genera i timestamp
    timestamps = pd.date_range(
        start=datetime.now(),
        periods=num_bars,
        freq=bar_interval
    )

    # Genera i prezzi
    returns = np.random.normal(0, volatility, num_bars)
    prices = initial_price * np.exp(np.cumsum(returns))

    # Genera i volumi con distribuzione lognormale
    volumes = np.random.lognormal(
        mean=np.log(volume_mean),
        sigma=0.5,
        size=num_bars
    )

    # Genera OHLCV
    df = pd.DataFrame(index=timestamps)
    df['close'] = prices
    df['volume'] = volumes

    # Genera open/high/low con rumore attorno al close
    noise = volatility * prices * 0.5
    df['open'] = df['close'].shift(1).fillna(initial_price) + np.random.normal(0, noise, num_bars)
    df['high'] = df[['open', 'close']].max(axis=1) + np.abs(np.random.normal(0, noise, num_bars))
    df['low'] = df[['open', 'close']].min(axis=1) - np.abs(np.random.normal(0, noise, num_bars))

    # Riordina le colonne
    df = df[['open', 'high', 'low', 'close', 'volume']]
    df.index.name = 'timestamp'

    # Calcola statistiche
    stats = {
        'price_stats': {
            'mean': df['close'].mean(),
            'std': df['close'].std(),
            'min': df['close'].min(),
            'max': df['close'].max()
        },
        'volume_stats': {
            'mean': df['volume'].mean(),
            'std': df['volume'].std(),
            'min': df['volume'].min(),
            'max': df['volume'].max()
        }
    }

    if output_file:
        df.to_parquet(output_file)

    return df, stats


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Generate synthetic OHLCV test data')
    parser.add_argument('output_file', help='Output file path')
    parser.add_argument('--bars', type=int, default=1000,
                       help='Number of bars to generate (default: 1000)')
    parser.add_argument('--interval', default='1min',
                       help='Bar interval (default: 1min)')
    parser.add_argument('--price', type=float, default=100.0,
                       help='Initial price (default: 100.0)')
    parser.add_argument('--volatility', type=float, default=0.02,
                       help='Daily volatility (default: 0.02)')
    parser.add_argument('--trend', type=float, default=0.0,
                       help='Daily trend/drift (default: 0.0)')
    parser.add_argument('--volume', type=float, default=1000.0,
                       help='Mean volume per bar (default: 1000.0)')
    parser.add_argument('--volume-std', type=float, default=200.0,
                       help='Volume standard deviation (default: 200.0)')
    parser.add_argument('--seed', type=int, default=None,
                       help='Random seed (default: None)')

    args = parser.parse_args()

    generate_test_data(
        output_file=args.output_file,
        num_bars=args.bars,
        bar_interval=args.interval,
        initial_price=args.price,
        volatility=args.volatility,
        trend=args.trend,
        volume_mean=args.volume,
        volume_std=args.volume_std,
        random_seed=args.seed
    )
