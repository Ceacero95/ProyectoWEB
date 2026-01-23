
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
    
    processed_months = set()
    current_date = start_date
    while current_date <= end_date:
        year = current_date.strftime("%Y")
        month = current_date.strftime("%m")
        month_key = f"{year}-{month}"
        
        if month_key in processed_months:
            current_date += timedelta(days=1)
            continue
            
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
                
            # Extend Schema with Metadata
            full_schema = LIQUICOMUN_SCHEMA[table_name].copy()
            full_schema.update({
                'periodo': 'INTEGER',
                'liquidacion': 'VARCHAR(10)',
                'source_file': 'TEXT',
                'fecha_proceso': 'TIMESTAMP',
                'resolucion': 'VARCHAR(5)'
            })
            
            # 1. Ensure Table Exists
            try:
                pk_cols = ['fecha', 'periodo', 'liquidacion', 'source_file']
                db_manager.create_table_if_not_exists(table_name, 'liquicomun', full_schema, pk_cols=pk_cols)
                db_manager.create_indexes(table_name, ['source_file'], schema='liquicomun')
            except Exception as e:
                 logger.error(f"Failed to ensure table {table_name}: {e}")
                 continue

            # 2. Cast Types
            for col, dtype in full_schema.items():
                if col not in df.columns:
                    df[col] = None
                
                if "NUMERIC" in dtype or "DECIMAL" in dtype:
                     df[col] = pd.to_numeric(df[col], errors='coerce')
                elif "DATE" in dtype:
                     # Spanish dates are DD/MM/YYYY, so we must use dayfirst=True
                     df[col] = pd.to_datetime(df[col], dayfirst=True, errors='coerce').dt.date
                elif "INTEGER" in dtype:
                     df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(int)
                     
            # 3. Filter rows with invalid dates (e.g. footers like '*')
            orig_len = len(df)
            df.dropna(subset=['fecha'], inplace=True)
            if len(df) < orig_len:
                logger.info(f"  Filtered {orig_len - len(df)} rows with NaT dates.")
                
            # 4. Filter future dates (Safety)
            from datetime import datetime
            today = datetime.now().date()
            df = df[df['fecha'] <= today]
            if len(df) < orig_len:
                 logger.info(f"  Filtered {orig_len - len(df)} rows (invalid dates or future dates > {today}).")

            # 5. Bulk Insert
            logger.info(f"  Inserting {len(df)} rows into {table_name}")
            
            # Ensure PK columns are not null
            df.dropna(subset=pk_cols, inplace=True)
            if df.empty:
                logger.warning(f"  Skipping {table_name}: all rows have null PKs")
                continue
                
            try:
                from sqlalchemy import text
                from src.common.database import get_engine
                
                engine = get_engine()
                
                # Robust Cleaning Strategy
                # For cumulative files (like A2), we should delete by (fecha, liquidacion) to avoid duplicates
                # when newer cumulative files cover the same dates.
                liqs = df['liquidacion'].unique()
                is_cumulative = any(l in ['A2', 'C2'] for l in liqs) # Expand as needed
                
                with engine.begin() as conn:
                    if is_cumulative:
                        logger.info(f"  Cumulative data detected ({liqs}). Deleting by (fecha, liquidacion)...")
                        # To be efficient, we delete per (date, liq) combination present in DF
                        for l in liqs:
                            relevant_dates = df[df['liquidacion'] == l]['fecha'].unique()
                            # Convert dates to string for SQL if needed, but SQLAlchemy handles it.
                            for d in relevant_dates:
                                conn.execute(
                                    text(f"DELETE FROM liquicomun.\"{table_name}\" WHERE fecha = :d AND liquidacion = :l"),
                                    {"d": d, "l": l}
                                )
                    else:
                        # Standard logic: delete by source_file
                        src_files = df['source_file'].unique()
                        for src in src_files:
                            conn.execute(
                                text(f"DELETE FROM liquicomun.\"{table_name}\" WHERE source_file = :src"),
                                {"src": src}
                            )
                            logger.info(f"  Cleaned existing data for source_file: {src}")

                db_manager.bulk_insert_df(df, table_name, schema='liquicomun', if_exists='append', pk_cols=pk_cols)
            except Exception as e:
                logger.error(f"  Insert failed: {e}")

        processed_months.add(month_key)
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
