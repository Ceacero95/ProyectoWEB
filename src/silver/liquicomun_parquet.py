
import logging
import argparse
import pandas as pd
import io
import re
import os
from datetime import datetime, timedelta
from src.silver.parser import DataParser
from src.common.filesystem import StorageManager
from src.config.liquicomun_schema import LIQUICOMUN_SCHEMA

logger = logging.getLogger(__name__)

def ingest_to_parquet(start_date: datetime, end_date: datetime):
    """
    Reads Bronze ZIPs, extracts PRDV files, and saves them as Parquet in Silver.
    """
    storage = StorageManager()
    
    current_date = start_date
    while current_date <= end_date:
        year = current_date.strftime("%Y")
        month = current_date.strftime("%m")
        date_str = current_date.strftime("%Y%m%d")
        
        bronze_dir = f"bronze/liquicomun/{year}/{month}"
        
        # List items in bronze dir (efficient listing)
        # Note: StorageManager.list_files returns RELATIVE paths from base_path?
        # Let's assume it returns relative paths to the input dir or full relative paths.
        # Based on previous usage: list_files(dir) returns list of file paths.
        
        try:
            files = storage.list_files(bronze_dir, extension=".zip")
        except FileNotFoundError:
            logger.warning(f"No directory {bronze_dir}")
            current_date += timedelta(days=1)
            continue

        # Filter for current date (optimization to allow granular runs)
        # Assuming filename format: esios_{id}_{yyyymmdd}.zip
        daily_files = [f for f in files if f"_{date_str}.zip" in f]
        
        for zip_path in daily_files:
            logger.info(f"Ingesting {zip_path} to Parquet...")
            content = storage.read(zip_path)
            if not content: continue
            
            # Use Parser to extract files from ZIP
            # subtype is usually 'liquicomun'
            subtype, extracted_files = DataParser.parse_liquicomun_zip(content)
            
            for file_name, file_content in extracted_files.items():
                low_name = file_name.lower()
                
                # Check for supported types
                valid_types = [
                    "prdvdatos", "prdvbaqh", "prdvsuqh",
                    "enrrqhba", "enrrqhsu", "enrttrba", "enrttrsu",
                    "ensecqhba", "ensecqhsu", "enterqhba", "enterqhsu"
                ]
                
                # Determine table type
                table_type = None
                for vt in valid_types:
                    if vt in low_name:
                        table_type = vt
                        break
                
                if not table_type: continue
                
                logger.info(f"  Processing {file_name} -> {table_type}")
                
                # --- PARSING LOGIC (Reused from fixed liquicomun.py) ---
                f_io = io.BytesIO(file_content)
                schema_def = LIQUICOMUN_SCHEMA.get(f"liq_{table_type}")
                if not schema_def:
                    logger.warning(f"No schema for liq_{table_type}")
                    continue
                schema_keys = list(schema_def.keys())

                try:
                    # Skip 2 rows for PRDV
                    df = pd.read_csv(
                        f_io, 
                        sep=';', 
                        header=None, 
                        skiprows=2, 
                        encoding='latin-1', 
                        on_bad_lines='skip', 
                        engine='python'
                    )
                    
                    df = df.dropna(axis=1, how='all') # Trim trailing
                    
                    # Ensure columns match schema length
                    if len(df.columns) > len(schema_keys):
                        df = df.iloc[:, :len(schema_keys)]
                    
                    if len(df.columns) == len(schema_keys):
                        df.columns = schema_keys
                    else:
                        logger.warning(f"    Column mismatch: Found {len(df.columns)}, expected {len(schema_keys)}")
                        # Best effort mapping
                        mapping = {df.columns[i]: schema_keys[i] for i in range(min(len(df.columns), len(schema_keys)))}
                        df.rename(columns=mapping, inplace=True)

                    # --- ENRICHMENT ---
                    base_only = os.path.basename(file_name)
                    liq_val = base_only[:2].upper()
                    
                    df['liquidacion'] = liq_val
                    df['source_file'] = file_name
                    df['fecha_proceso'] = datetime.now()
                    
                    # Ensure numeric for date components
                    for c in ['hora', 'qh']:
                        if c in df.columns:
                            df[c] = pd.to_numeric(df[c], errors='coerce').fillna(0).astype(int)
                            
                    # Calculate Periodo (1-96)
                    if 'hora' in df.columns and 'qh' in df.columns:
                        df['periodo'] = (df['hora'] - 1) * 4 + df['qh']
                    else:
                        df['periodo'] = 1 # Fallback
                        
                    # Resolucion logic
                    df['resolucion'] = 'QH' if 'qh' in df.columns else 'H'

                    # --- WRITE PARQUET ---
                    # Path: silver/liquicomun/{year}/{month}/{table_type}_{liq_val}_{timestamp}.parquet
                    # Using timestamp to avoid collisions if multiple files match (though unlikely with smart DL)
                    
                    # Clean filename for parquet
                    safe_name = os.path.splitext(file_name)[0]
                    parquet_name = f"{safe_name}.parquet"
                    silver_path = f"silver/liquicomun/{year}/{month}/{parquet_name}"
                    
                    # We need a way to write dataframe to storage
                    # StorageManager doesn't have write_parquet.
                    # We can get full path from StorageManager?
                    # StorageManager._get_full_path is internal.
                    # But we can assume local storage for now or use PyArrow buffer?
                    
                    # To allow StorageManager abstraction, ideally we write to buffer then save(bytes).
                    buf = io.BytesIO()
                    df.to_parquet(buf, index=False)
                    storage.save(silver_path, buf.getvalue())
                    logger.info(f"    Saved Parquet: {silver_path}")

                except Exception as e:
                    logger.error(f"    Error parsing {file_name}: {e}")
                    continue

        current_date += timedelta(days=1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--start-date", required=True)
    parser.add_argument("--end-date", required=True)
    args = parser.parse_args()
    
    start = datetime.strptime(args.start_date, "%Y-%m-%d")
    end = datetime.strptime(args.end_date, "%Y-%m-%d")
    
    logging.basicConfig(level=logging.INFO)
    ingest_to_parquet(start, end)
