
import os
import pandas as pd
from pathlib import Path

def get_dir_size(path):
    total = 0
    for p in Path(path).rglob('*'):
        if p.is_file():
            total += p.stat().st_size
    return total

def estimate_db_rows():
    # Helper to count rows in parquet files as a proxy for DB rows
    silver_path = Path("local_data/silver")
    total_rows = 0
    if not silver_path.exists():
        return 0
        
    for p in silver_path.rglob('*.parquet'):
        try:
            # We don't need to read whole file, but parquet metadata reading is not standard in os
            # Fast way: read distinct dates? No, just sum file sizes and assume ratio?
            # Or simplified: Read it.
            df = pd.read_parquet(p, columns=[]) # Fast read
            total_rows += len(df)
        except:
            pass
    return total_rows

bronze_size = get_dir_size("local_data/bronze")
silver_size = get_dir_size("local_data/silver")
logs_size = get_dir_size("logs")

# DB Size Estimation
# Postgres usually 2x-3x the Parquet size due to indexes and row overhead
# or 1GB per ~5-10M rows depending on width.
# Let's count rows if possible, else use silver_size * 3

print(f"Bronze (Compressed ZIPs): {bronze_size / (1024*1024):.2f} MB")
print(f"Silver (Parquet): {silver_size / (1024*1024):.2f} MB")
print(f"Logs: {logs_size / (1024*1024):.2f} MB")

# Attempt row count estimate (might be slow if many files, let's try direct approach or fallback)
try:
    rows = estimate_db_rows()
    print(f"Estimated Total Rows: {rows}")
except Exception as e:
    print(f"Could not count rows: {e}")
