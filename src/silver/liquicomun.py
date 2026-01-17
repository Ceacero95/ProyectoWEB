
import logging
import argparse
import pandas as pd
import io
import os
import re
from datetime import datetime, timedelta
from src.common.filesystem import StorageManager
from src.common.database import DatabaseManager
from src.config.liquicomun_schema import LIQUICOMUN_SCHEMA

logger = logging.getLogger(__name__)

def process_liquicomun(start_date: datetime, end_date: datetime):
    """
    Loads Parquet files from Silver layer into Gold DB.
    Current scope: PRDV files.
    """
    storage = StorageManager()
    db_manager = DatabaseManager()
    
    current_date = start_date
    while current_date <= end_date:
        year = current_date.strftime("%Y")
        month = current_date.strftime("%m")
        silver_dir = f"silver/liquicomun/{year}/{month}"
        
        try:
            files = storage.list_files(silver_dir, extension=".parquet")
        except FileNotFoundError:
            logger.info(f"No silver data for {silver_dir}")
            current_date += timedelta(days=1)
            continue
            
        for parquet_file in files:
            base_name = os.path.basename(parquet_file).lower()
            
            # Identify table
            # Identify table
            table_name = None
            valid_types = [
                "prdvdatos", "prdvbaqh", "prdvsuqh",
                "enrrqhba", "enrrqhsu", "enrttrba", "enrttrsu",
                "ensecqhba", "ensecqhsu", "enterqhba", "enterqhsu"
            ]
            
            for vt in valid_types:
                if vt.lower() in base_name:
                    table_name = f"liq_{vt.lower()}"
                    break
            
            if not table_name:
                continue
                
            logger.info(f"Loading {parquet_file} into {table_name}...")
            
            content = storage.read(parquet_file)
            if not content: continue
            
            try:
                df = pd.read_parquet(io.BytesIO(content))
            except Exception as e:
                logger.error(f"Failed to read parquet {parquet_file}: {e}")
                continue
            
            if df.empty:
                continue
                
            # --- DATABASE INSERTION ---
            if table_name not in LIQUICOMUN_SCHEMA:
                logger.error(f"Schema not found for {table_name}")
                continue
                
            schema_def = LIQUICOMUN_SCHEMA[table_name]
            
            # 1. Ensure Table Exists
            try:
                # Use liquicomun schema
                # PK: Fecha, Periodo, Liquidacion, Source_File
                pk_cols = ['fecha', 'periodo', 'liquidacion', 'source_file']
                db_manager.create_table_if_not_exists(table_name, 'liquicomun', schema_def, pk_cols=pk_cols)
                
                # Ensure index on source_file
                db_manager.create_indexes(table_name, ['source_file'], schema='liquicomun')
            except Exception as e:
                 logger.error(f"Failed to ensure table {table_name}: {e}")
                 continue

            # 2. Cast Types
            for col, dtype in schema_def.items():
                if col not in df.columns:
                    df[col] = None
                
                if "NUMERIC" in dtype or "DECIMAL" in dtype:
                     df[col] = pd.to_numeric(df[col], errors='coerce')
                elif "DATE" in dtype:
                     df[col] = pd.to_datetime(df[col], dayfirst=True, errors='coerce').dt.date
                elif "INTEGER" in dtype:
                     df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(int)
                     
            # 3. Bulk Insert
            logger.info(f"  Inserting {len(df)} rows into {table_name}")
            
            # Ensure PK columns are not null
            df.dropna(subset=pk_cols, inplace=True)
            if df.empty:
                logger.warning(f"  Skipping {table_name}: all rows have null PKs")
                continue
                
            try:
                # Clean up existing data for this source file to avoid duplicates
                from sqlalchemy import text
                from src.common.database import get_engine
                
                # Check if source_file column exists and delete if so
                # We assume it exists based on schema, but safety check is good or just try/except
                clean_sql = text(f"DELETE FROM liquicomun.\"{table_name}\" WHERE source_file = :src")
                
                # Get unique source files in this batch (should be just one usually)
                src_files = df['source_file'].unique()
                engine = get_engine()
                with engine.begin() as conn:
                    for src in src_files:
                        conn.execute(clean_sql, {"src": src})
                        logger.info(f"  Cleaned existing data for source_file: {src}")

                db_manager.bulk_insert_df(df, table_name, schema='liquicomun', if_exists='append', pk_cols=pk_cols)
            except Exception as e:
                logger.error(f"  Insert failed: {e}")

        current_date += timedelta(days=1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--start-date", required=True)
    parser.add_argument("--end-date", required=True)
    args = parser.parse_args()
    
    start = datetime.strptime(args.start_date, "%Y-%m-%d")
    end = datetime.strptime(args.end_date, "%Y-%m-%d")
    
    logging.basicConfig(level=logging.INFO)
    process_liquicomun(start, end)
