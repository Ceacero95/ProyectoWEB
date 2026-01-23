import sys
import os
from datetime import datetime
import traceback

# Force unbuffered output
sys.stdout.reconfigure(line_buffering=True)
sys.stderr.reconfigure(line_buffering=True)

print("--- DEBUG START ---")

try:
    print("Importing modules...")
    sys.path.append("/opt/airflow")
    from src.common.database import get_engine, DatabaseManager
    from src.bronze.omie.pdbc import download_pdbc
    from src.silver.omie.pdbc import process_pdbc
    from src.bronze.omie.pdbf import download_pdbf
    from src.silver.omie.pdbf import process_pdbf
    from src.bronze.omie.pdvd import download_pdvd
    from src.silver.omie.pdvd import process_pdvd
    from src.bronze.omie.marginalpdbc import download_marginalpdbc
    from src.silver.omie.marginalpdbc import process_marginalpdbc
    from src.bronze.omie.marginalpibc import download_marginalpibc
    from src.silver.omie.marginalpibc import process_marginalpibc
    from src.common.monitoring import MonitoringManager
    print("Imports OK")
except Exception as e:
    print(f"Import Error: {e}")
    traceback.print_exc()
    sys.exit(1)

def run_flow():
    start = datetime(2025, 1, 1)
    end = datetime(2025, 1, 2) # Short range
    
    tasks = [
        ("PDBC", download_pdbc, process_pdbc),
        ("PDBF", download_pdbf, process_pdbf),
        ("PDVD", download_pdvd, process_pdvd),
        ("MarginalPDBC", download_marginalpdbc, process_marginalpdbc),
        ("MarginalPIBC", download_marginalpibc, process_marginalpibc),
    ]

    for name, down_func, proc_func in tasks:
        print(f"--- Running {name} ---")
        try:
            print(f"Downloading {name}...")
            down_func(start, end)
            print(f"Processing {name}...")
            proc_func(start, end)
            print(f"{name} Completed.")
        except Exception as e:
            print(f"{name} Failed: {e}")
            traceback.print_exc()
            raise

    print("--- Running Monitoring ---")
    try:
        mon = MonitoringManager()
        # Test just one for now, or all
        for t in ["pdbc", "pdbf", "pdvd", "marginalpdbc", "marginalpibc"]:
             print(f"Monitoring {t}...")
             mon.update_control_table(t, "omie")
        print("Monitoring Completed.")
    except Exception as e:
        print(f"Monitoring Failed: {e}")
        traceback.print_exc()
        raise

if __name__ == "__main__":
    try:
        run_flow()
        print("ALL TESTS PASSED")
    except Exception as e:
        print("TEST SUITE FAILED")
        sys.exit(1)
