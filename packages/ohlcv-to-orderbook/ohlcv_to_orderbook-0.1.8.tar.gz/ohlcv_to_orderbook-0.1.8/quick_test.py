#!/usr/bin/env python3
"""Test rapido per verificare la correzione dei volumi."""

import pandas as pd
from ohlcv_to_orderbook.config import OrderbookConfig
from ohlcv_to_orderbook.ohlcv_to_orderbook import OrderbookGenerator
from ohlcv_to_orderbook.orderbook_to_ohlcv import OHLCVGenerator

def test_volume_correction():
    """Test veloce della correzione dei volumi."""

    # Crea dati OHLCV di test semplici
    test_data = pd.DataFrame({
        'timestamp': pd.date_range('2025-01-01', periods=3, freq='1min'),
        'open': [100.0, 101.0, 102.0],
        'high': [100.5, 101.5, 102.5],
        'low': [99.5, 100.5, 101.5],
        'close': [101.0, 102.0, 103.0],
        'volume': [1000.0, 1500.0, 2000.0]
    })

    print(f"📊 Dati originali - Volume totale: {test_data['volume'].sum()}")

    # Genera orderbook con size_distribution_factor = 0.3
    config = OrderbookConfig(size_distribution_factor=0.3)
    generator = OrderbookGenerator(config=config)

    orderbook_df = generator.generate_orderbook_data(test_data, points_per_bar=4)
    total_orderbook_volume = orderbook_df['bid_size'].sum() + orderbook_df['ask_size'].sum()

    print(f"📈 Orderbook generato - Volume totale: {total_orderbook_volume:.2f}")

    # Ricostruisci OHLCV CON compensazione
    converter_with_compensation = OHLCVGenerator(size_distribution_factor=0.3)
    reconstructed_with_comp = converter_with_compensation.group_orderbook_to_bars(orderbook_df)

    print(f"🔄 OHLCV ricostruito (CON compensazione) - Volume totale: {reconstructed_with_comp['volume'].sum():.2f}")

    # Ricostruisci OHLCV SENZA compensazione (per confronto)
    converter_without_compensation = OHLCVGenerator()
    reconstructed_without_comp = converter_without_compensation.group_orderbook_to_bars(orderbook_df)

    print(f"❌ OHLCV ricostruito (SENZA compensazione) - Volume totale: {reconstructed_without_comp['volume'].sum():.2f}")

    # Calcola le differenze
    original_total = test_data['volume'].sum()
    with_comp_diff = abs(reconstructed_with_comp['volume'].sum() - original_total) / original_total * 100
    without_comp_diff = abs(reconstructed_without_comp['volume'].sum() - original_total) / original_total * 100

    print(f"\n📊 RISULTATI:")
    print(f"✅ Differenza CON compensazione: {with_comp_diff:.2f}%")
    print(f"❌ Differenza SENZA compensazione: {without_comp_diff:.2f}%")

    if with_comp_diff < 5:
        print("🎉 CORREZIONE RIUSCITA! La compensazione dei volumi funziona correttamente.")
        return True
    else:
        print("⚠️  La correzione non è completamente efficace.")
        return False

if __name__ == "__main__":
    test_volume_correction()
