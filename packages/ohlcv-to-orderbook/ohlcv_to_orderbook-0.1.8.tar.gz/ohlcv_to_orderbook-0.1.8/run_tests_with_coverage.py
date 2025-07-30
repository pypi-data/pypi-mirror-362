#!/usr/bin/env python3
"""
Script per eseguire i test con coverage.
Uso: python run_tests_with_coverage.py
"""
import subprocess
import sys

def run_tests_with_coverage():
    """Esegue i test con coverage completo."""
    cmd = [
        sys.executable, "-m", "pytest",
        "--cov=ohlcv_to_orderbook",
        "--cov-report=term-missing",
        "--cov-report=html:htmlcov",
        "--cov-report=xml:coverage.xml",
        "--cov-fail-under=80",
        "--cov-branch",
        "tests/"
    ]

    print("🧪 Eseguendo test con coverage...")
    print(f"Comando: {' '.join(cmd)}")
    print("-" * 50)

    try:
        result = subprocess.run(cmd, check=False)
        if result.returncode == 0:
            print("\n✅ Test completati con successo!")
            print("📊 Report coverage disponibile in htmlcov/index.html")
        else:
            print("\n❌ Alcuni test sono falliti o coverage insufficiente")
        return result.returncode
    except Exception as e:
        print(f"\n💥 Errore durante l'esecuzione: {e}")
        return 1

if __name__ == "__main__":
    exit_code = run_tests_with_coverage()
    sys.exit(exit_code)
