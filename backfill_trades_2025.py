
import os
import sys
import logging
from datetime import datetime

# Add project root to path
sys.path.append(os.getcwd())

# Configuration logger
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("backfill_trades_2025.log"),
        logging.StreamHandler()
    ]
)

from src.bronze.omie.trades import download_trades
from src.silver.omie.trades import process_trades

def backfill():
    # Process full year 2025
    start_date = datetime(2025, 1, 1)
    end_date = datetime(2025, 12, 31)
    
    print(f"--- 1. Downloading Trades for 2025 ({start_date.date()} - {end_date.date()}) ---")
    download_trades(start_date, end_date)
    
    print(f"\n--- 2. Processing Trades for 2025 ({start_date.date()} - {end_date.date()}) ---")
    process_trades(start_date, end_date)
    
    print("\n--- Backfill Done ---")

if __name__ == "__main__":
    backfill()
