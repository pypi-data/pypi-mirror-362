#!/usr/bin/env python3
"""Test completo del sistema OHLCV-to-Orderbook."""

import os
import sys
import traceback
from datetime import datetime
from typing import Dict, Any

import pandas as pd
import numpy as np

# Aggiungi il percorso del progetto
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ohlcv_to_orderbook.config import OrderbookConfig
from ohlcv_to_orderbook.ohlcv_to_orderbook import OrderbookGenerator, OrderbookValidator
from ohlcv_to_orderbook.orderbook_to_ohlcv import OHLCVGenerator
from ohlcv_to_orderbook.synthetic_data import generate_test_data
from ohlcv_to_orderbook.data_types import ValidationConfig


def print_header(title: str):
    """Stampa un header formattato."""
    print(f"\n{'='*60}")
    print(f"{title:^60}")
    print(f"{'='*60}")


def print_test_result(test_name: str, success: bool, details: str = ""):
    """Stampa il risultato di un test."""
    status = "✅ PASSATO" if success else "❌ FALLITO"
    print(f"{test_name}: {status}")
    if details:
        print(f"   {details}")


def test_basic_functionality():
    """Test basic functionality."""
    print_header("TEST FUNZIONALITÀ DI BASE")

    results: Dict[str, int] = {"passed": 0, "failed": 0}

    try:
        # Test 1: Generazione dati sintetici
        print("\n1. Test generazione dati sintetici...")
        df, stats = generate_test_data(
            output_file='test_synthetic.parquet',
            num_bars=10,
            bar_interval='1min',
            random_seed=42
        )

        assert len(df) == 10, "Numero di barre non corretto"
        assert all(col in df.columns for col in ['open', 'high', 'low', 'close', 'volume']), "Colonne mancanti"
        assert (df['high'] >= df['low']).all(), "High < Low rilevato"

        print_test_result("Generazione dati sintetici", True, f"Generati {len(df)} bars")
        results["passed"] += 1

        # Test 2: Configurazione OrderbookGenerator
        print("\n2. Test configurazione OrderbookGenerator...")
        config = OrderbookConfig(
            spread_percentage=0.001,
            size_distribution_factor=0.3
        )
        generator = OrderbookGenerator(config=config)

        assert generator.config.spread_percentage == 0.001, "Spread percentage non corretto"
        assert generator.config.size_distribution_factor == 0.3, "Size distribution factor non corretto"

        print_test_result("Configurazione OrderbookGenerator", True)
        results["passed"] += 1

        # Test 3: Generazione orderbook
        print("\n3. Test generazione orderbook...")
        orderbook_df = generator.generate_orderbook_data(df, points_per_bar=4)

        expected_rows = len(df) * 4
        assert len(orderbook_df) == expected_rows, f"Attese {expected_rows} righe, ottenute {len(orderbook_df)}"

        required_cols = ['timestamp', 'bid_price', 'ask_price', 'bid_size', 'ask_size', 'mid_price']
        assert all(col in orderbook_df.columns for col in required_cols), "Colonne orderbook mancanti"

        print_test_result("Generazione orderbook", True, f"Generati {len(orderbook_df)} records")
        results["passed"] += 1

        # Test 4: Ricostruzione OHLCV
        print("\n4. Test ricostruzione OHLCV...")
        converter = OHLCVGenerator(size_distribution_factor=0.3)
        reconstructed_df = converter.group_orderbook_to_bars(orderbook_df)

        assert len(reconstructed_df) == len(df), "Numero di barre ricostruite non corretto"

        print_test_result("Ricostruzione OHLCV", True, f"Ricostruite {len(reconstructed_df)} bars")
        results["passed"] += 1

        # Test 5: Validazione accuratezza
        print("\n5. Test validazione accuratezza...")
        validation_config = ValidationConfig(price_tolerance=0.005)  # 0.5% tolerance
        validator = OrderbookValidator(config=validation_config)

        # Confronta i prezzi
        price_errors = 0
        for col in ['open', 'high', 'low', 'close']:
            diff_pct = ((reconstructed_df[col] - df[col]) / df[col] * 100).abs()
            max_diff = float(diff_pct.max())
            if max_diff > 0.5:
                price_errors += 1

        # Confronta i volumi
        vol_diff_pct = ((reconstructed_df['volume'] - df['volume']) / df['volume'] * 100).abs()
        max_vol_diff = float(vol_diff_pct.max())

        success = price_errors == 0 and max_vol_diff < 30.0
        max_price_diffs = []
        for col in ['open', 'high', 'low', 'close']:
            diff_pct = ((reconstructed_df[col] - df[col]) / df[col] * 100).abs()
            max_price_diffs.append(float(diff_pct.max()))
        max_price_diff = max(max_price_diffs)
        details = f"Max diff prezzi: {max_price_diff:.3f}%, Max diff volume: {max_vol_diff:.1f}%"

        print_test_result("Validazione accuratezza", success, details)
        if success:
            results["passed"] += 1
        else:
            results["failed"] += 1

        # Cleanup
        if os.path.exists('test_synthetic.parquet'):
            os.remove('test_synthetic.parquet')

    except Exception as e:
        print_test_result("Test base", False, f"Errore: {str(e)}")
        results["failed"] += 1
        print(f"Traceback completo:\n{traceback.format_exc()}")

    return results


def test_performance_scalability():
    """Test performance and scalability."""
    print_header("TEST PERFORMANCE E SCALABILITÀ")

    results: Dict[str, int] = {"passed": 0, "failed": 0}

    try:
        # Test con dataset più grandi
        for num_bars in [100, 500]:
            print(f"\nTest con {num_bars} bars...")
            start_time = datetime.now()

            df, _ = generate_test_data(
                output_file=f'test_perf_{num_bars}.parquet',
                num_bars=num_bars,
                random_seed=42
            )

            config = OrderbookConfig(size_distribution_factor=0.3)
            generator = OrderbookGenerator(config=config)
            orderbook_df = generator.generate_orderbook_data(df, points_per_bar=4)

            converter = OHLCVGenerator(size_distribution_factor=0.3)
            reconstructed_df = converter.group_orderbook_to_bars(orderbook_df)

            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()

            success = duration < 30.0  # Deve completare in meno di 30 secondi
            print_test_result(f"Performance {num_bars} bars", success, f"Completato in {duration:.2f}s")

            if success:
                results["passed"] += 1
            else:
                results["failed"] += 1

            # Cleanup
            if os.path.exists(f'test_perf_{num_bars}.parquet'):
                os.remove(f'test_perf_{num_bars}.parquet')

    except Exception as e:
        print_test_result("Test performance", False, f"Errore: {str(e)}")
        results["failed"] += 1

    return results


def test_edge_cases():
    """Test di casi limite."""
    print_header("TEST CASI LIMITE")

    results: Dict[str, int] = {"passed": 0, "failed": 0}

    try:
        # Test 1: Dati con valori estremi
        print("\n1. Test con valori estremi...")
        extreme_data = pd.DataFrame({
            'timestamp': pd.date_range('2025-01-01', periods=3, freq='1min'),
            'open': [0.001, 10000.0, 50.0],
            'high': [0.002, 10001.0, 55.0],
            'low': [0.0005, 9999.0, 45.0],
            'close': [0.0015, 10000.5, 52.0],
            'volume': [1.0, 1000000.0, 500.0]
        })

        config = OrderbookConfig(size_distribution_factor=0.3)
        generator = OrderbookGenerator(config=config)
        orderbook_df = generator.generate_orderbook_data(extreme_data, points_per_bar=2)

        converter = OHLCVGenerator(size_distribution_factor=0.3)
        reconstructed_df = converter.group_orderbook_to_bars(orderbook_df)

        assert len(reconstructed_df) == len(extreme_data), "Ricostruzione con valori estremi fallita"
        print_test_result("Valori estremi", True)
        results["passed"] += 1

        # Test 2: Dataset minimo
        print("\n2. Test con dataset minimo...")
        minimal_data = pd.DataFrame({
            'timestamp': [pd.Timestamp('2025-01-01')],
            'open': [100.0],
            'high': [101.0],
            'low': [99.0],
            'close': [100.5],
            'volume': [1000.0]
        })

        orderbook_df = generator.generate_orderbook_data(minimal_data, points_per_bar=2)
        reconstructed_df = converter.group_orderbook_to_bars(orderbook_df)

        assert len(reconstructed_df) == 1, "Ricostruzione dataset minimo fallita"
        print_test_result("Dataset minimo", True)
        results["passed"] += 1

    except Exception as e:
        print_test_result("Test casi limite", False, f"Errore: {str(e)}")
        results["failed"] += 1
        print(f"Traceback completo:\n{traceback.format_exc()}")

    return results


def main():
    """Esegue tutti i test."""
    print_header("AVVIO TEST COMPLETO SISTEMA OHLCV-TO-ORDERBOOK")

    total_results: Dict[str, int] = {"passed": 0, "failed": 0}

    # Esegui tutti i test
    test_functions = [
        test_basic_functionality,
        test_performance_scalability,
        test_edge_cases
    ]

    for test_func in test_functions:
        try:
            results = test_func()
            total_results["passed"] += results["passed"]
            total_results["failed"] += results["failed"]
        except Exception as e:
            print(f"Errore nell'esecuzione di {test_func.__name__}: {str(e)}")
            total_results["failed"] += 1

    # Stampa risultati finali
    print_header("RISULTATI FINALI")
    total_tests = total_results["passed"] + total_results["failed"]
    success_rate = (total_results["passed"] / total_tests * 100) if total_tests > 0 else 0

    print(f"\n📊 STATISTICHE COMPLETE:")
    print(f"   Test eseguiti: {total_tests}")
    print(f"   Test passati: {total_results['passed']} ✅")
    print(f"   Test falliti: {total_results['failed']} ❌")
    print(f"   Tasso di successo: {success_rate:.1f}%")

    if total_results["failed"] == 0:
        print(f"\n🎉 TUTTI I TEST SONO PASSATI! Il sistema è funzionante.")
        return 0
    else:
        print(f"\n⚠️  ALCUNI TEST SONO FALLITI. Verificare i dettagli sopra.")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
