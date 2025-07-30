# Copilot Instructions

## Scopo del Progetto
Questo progetto converte dati OHLCV (Open, High, Low, Close, Volume) in file Parquet in una rappresentazione sintetica dell'orderbook di primo livello (best bid/ask) e viceversa, per validare la correttezza della conversione.

## Fasi del Progetto

**Fase 1: Setup e struttura del progetto** ✅
- Creata la struttura delle cartelle (`ohlcv_to_orderbook/`, `tests/`).
- Inizializzato ambiente Python 3.8+ con dipendenze (`pandas`, `pyarrow`, `pytest`) utilizzando `uv` come gestore di ambiente e pacchetti.
- Configurato `pyproject.toml` per la gestione del progetto.

**Fase 2: Implementazione conversione OHLCV → Orderbook** ✅
- Implementata la classe `OrderbookGenerator` in `ohlcv_to_orderbook/ohlcv_to_orderbook.py`.
- Aggiunta validazione dei dati e gestione degli errori.
- Implementato algoritmo di stima del percorso dei prezzi basato sulla logica Open-High-Low vs Open-Low-High.

**Fase 3: Implementazione conversione Orderbook → OHLCV** ✅
- Implementata la classe `OHLCVGenerator` in `ohlcv_to_orderbook/orderbook_to_ohlcv.py`.
- Mantenuta coerenza con la funzione precedente (tipi, docstring, modularità).

**Fase 4: Gestione I/O Parquet** ✅
- Implementata la classe `ParquetHandler` in `ohlcv_to_orderbook/io_handlers.py`.
- Supporto completo per lettura/scrittura Parquet con `pyarrow` e `pandas`.

**Fase 5: Generazione dati di test sintetici** ✅
- Implementata funzione `generate_test_data` in `ohlcv_to_orderbook/synthetic_data.py`.
- Generazione di dati OHLCV e orderbook sintetici per i test.

**Fase 6: Test automatici** ✅
- Implementati test completi in `tests/test_conversions.py` e `tests/test_pipeline.py`.
- Validazione delle conversioni andata e ritorno con `pytest`.
- Aggiunta copertura dei test con `pytest-cov`.

**Fase 7: Refactoring e best practice** ✅
- Migliorata modularità con separazione delle responsabilità.
- Aggiunta tipizzazione completa con supporto `mypy`.
- Implementate configurazioni personalizzabili tramite `OrderbookConfig`.

**Fase 8: Creazione pipeline github** ✅
- Pipeline implementata localmente con script di test.
- Configurazione per CI/CD pronta per implementazione su GitHub.

**Fase 9: Documentazione** ✅
- Creato `README.md` completo con panoramica, installazione e utilizzo.
- Aggiornato `copilot_instructions.md` con dettagli implementativi.
- Tutte le istruzioni e commenti nel codice sono in inglese.

**Fase 10: Interfaccia Command Line (CLI)** ✅
- Creare classe `CLIRunner` in `ohlcv_to_orderbook/cli.py` per esecuzione da riga di comando.
- Supportare conversioni bidirezionali con parametri configurabili.
- Implementare argparse per gestione argomenti e opzioni CLI.
- Aggiungere entry point in `pyproject.toml` per comando `ohlcv-converter`.
- Includere opzioni per: file input/output, configurazione spread, numero di punti, precisione decimale, validazione, verbose mode.
- aggiorna l'istruzione d'uso nel `README.md` per includere la CLI.
- crea un test specifico per la CLI in `tests/test_cli.py`.

**Fase 11: Pubblicazione su PyPI** ✅
- Preparare il pacchetto per la pubblicazione su PyPI.
- Aggiornare `pyproject.toml` con metadata per PyPI.
- Testare l'installazione del pacchetto da PyPI.
- Aggiungere istruzioni per l'installazione da PyPI nel `README.md`.
- Assicurarsi che la documentazione sia completa e aggiornata.
- Verificare che tutti i test passino prima della pubblicazione.
- Creare un changelog per le versioni future.
- Assicurarsi che il codice sia conforme agli standard PEP 8 e che sia ben documentato.
- Aggiungere badge di stato del progetto (build, test, coverage) nel `README.md`.
- Aggiornare github actions per eseguire test e build automaticamente su push e pull request.
- Aggiornare github actions per eseguire il deploy su PyPI automaticamente al rilascio di una nuova versione.
- Aggiungere un file `CONTRIBUTING.md` per linee guida sui contributi al progetto.
- Aggiungere un file `LICENSE` per specificare la licenza del progetto (MIT).


## Dettagli Implementativi

### Architettura del Progetto

Il progetto è strutturato in moduli specializzati:

- **`data_types.py`**: Definizioni dei tipi con `TypedDict` per OHLCV e OrderBook
- **`config.py`**: Classe `OrderbookConfig` per parametri configurabili
- **`exceptions.py`**: Eccezioni personalizzate per gestione errori
- **`io_handlers.py`**: Gestione I/O Parquet con `ParquetHandler`
- **`ohlcv_to_orderbook.py`**: Conversione OHLCV → Orderbook con `OrderbookGenerator`
- **`orderbook_to_ohlcv.py`**: Conversione Orderbook → OHLCV con `OHLCVGenerator`
- **`synthetic_data.py`**: Generazione dati di test

### Algoritmo di Conversione OHLCV → Orderbook

L'algoritmo implementa la logica specificata per la stima del percorso dei prezzi:

1. **Determinazione del Percorso**:
   - Se `|Open - High| < |Open - Low|`: percorso Open → High → Low → Close
   - Altrimenti: percorso Open → Low → High → Close

2. **Generazione Spread**:
   - Calcolo spread dinamico basato su volatilità (High-Low)
   - Parametri configurabili per min/max spread in basis points

3. **Distribuzione Volume**:
   - Distribuzione uniforme o pesata del volume totale
   - Generazione di snapshot temporali all'interno della barra

### Configurazione

La classe `OrderbookConfig` permette di personalizzare:

```python
config = OrderbookConfig(
    min_spread_bps=1.0,          # Spread minimo in basis points
    max_spread_bps=10.0,         # Spread massimo in basis points
    volume_distribution='uniform', # Metodo distribuzione volume
    price_precision=2,           # Precisione decimale prezzi
    volume_precision=8,          # Precisione decimale volumi
    snapshots_per_bar=4          # Snapshot per barra OHLCV
)
```

### Validazione e Test

Il sistema include:

- **Validazione input**: Controllo formato e coerenza dati OHLCV
- **Test round-trip**: Verifica integrità conversione andata/ritorno
- **Test prestazioni**: Validazione su dataset di grandi dimensioni
- **Coverage testing**: Copertura completa del codice

### Utilizzo Avanzato

#### Esempio Pipeline Completa

```python
from ohlcv_to_orderbook import OrderbookGenerator, OHLCVGenerator
from ohlcv_to_orderbook.io_handlers import ParquetHandler
from ohlcv_to_orderbook.config import OrderbookConfig

# Configurazione personalizzata
config = OrderbookConfig(min_spread_bps=2.0, max_spread_bps=15.0)

# Inizializzazione componenti
orderbook_gen = OrderbookGenerator(config=config)
ohlcv_gen = OHLCVGenerator()
io_handler = ParquetHandler()

# Pipeline completa
ohlcv_data = io_handler.read_ohlcv("input.parquet")
orderbook_data = orderbook_gen.generate_orderbook(ohlcv_data)
io_handler.write_orderbook(orderbook_data, "orderbook.parquet")

# Validazione round-trip
reconstructed = ohlcv_gen.generate_ohlcv(orderbook_data)
validation_passed = orderbook_gen.validate_reconstruction(
    ohlcv_data, reconstructed, tolerance=0.001
)
```

#### Gestione Errori

Il sistema utilizza eccezioni specifiche:

- `ValidationError`: Errori di validazione dati
- `OrderbookGenerationError`: Errori nella generazione orderbook
- `IOError`: Errori I/O Parquet

### Estensibilità

Il design modulare permette:

- Aggiunta di nuovi formati I/O (CSV, JSON, etc.)
- Implementazione di strategie di spread alternative
- Integrazione con feed di dati real-time
- Estensione a orderbook multi-livello (L2, L3)

## Istruzioni d'Uso

### Installazione

```bash
pip install -e .
```

### Esecuzione Test

```bash
# Test completi
python run_tests_with_coverage.py

# Test specifici
pytest tests/test_conversions.py -v

# Test rapidi
python quick_test.py
```

### Controllo Qualità Codice

```bash
# Type checking
mypy ohlcv_to_orderbook/

# Coverage report
pytest --cov=ohlcv_to_orderbook --cov-report=html tests/
```

## Note Tecniche

- **Compatibilità**: Python 3.8+
- **Dipendenze core**: pandas≥2.0.0, pyarrow≥10.0.0, numpy≥1.21.0
- **Type safety**: Completa tipizzazione con mypy
- **Performance**: Ottimizzato per dataset di grandi dimensioni
- **Memory efficiency**: Gestione efficiente della memoria con chunking per file grandi

## Python Environment Management
- **Required**: `uv` package manager for Python
- Use `uv` for environment creation, package installation and dependency management
- Preferred over pip/venv for improved performance and dependency resolution
- Required for consistent environment setup across all development phases
**Basic uv Commands**:
```bash
# Install uv
pip install uv
# Create a new virtual environment
uv venv
# Activate the environment (macOS/Linux)
source .venv/bin/activate
# Install dependencies
uv pip install -r requirements.txt
# Install a package
uv pip install package_name
# Install development dependencies
uv pip install -e ".[dev]"
# Export dependencies to requirements.txt
uv pip freeze > requirements.txt
```
**Key uv Benefits**:
- Significantly faster than pip (10-100x)
- Reliable dependency resolution
- Reproducible environments
- Compatible with standard Python tooling
- Improved caching and parallel downloads
