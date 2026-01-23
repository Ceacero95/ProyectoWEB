
"""
data_processing/silver/omie/trades.py

OBJECTIVE:
    Parses and processes key 'Trades' files from OMIE.
    This module transforms raw CSV content (from ZIPs) into a structured format
    ready for database ingestion.

KEY FEATURES:
    - **Parsing**: Handles latin-1 encoding and skips metadata rows.
    - **Normalization**: Uses Regex to standardise column names (handling tabs/spaces).
    - **Idempotency**: Deletes existing records for the specific date before inserting to prevent duplicates.
    - **Storage**: Saves a copy in Parquet (Silver) and loads into PostgreSQL (Gold/Serving).

"""
import logging
import pandas as pd
from datetime import datetime, timedelta
import io
import zipfile
import re
from sqlalchemy import text
from src.common.filesystem import StorageManager
from src.common.database import DatabaseManager, get_engine

logger = logging.getLogger(__name__)

def parse_trades_content(content: bytes, filename: str) -> pd.DataFrame:
    """
    Parses the raw bytes of a single OMIE trades file (CSV-like).
    
    Logic:
    1. Decodes 'latin-1'.
    2. Skips first 2 lines (Metadata/Empty).
    3. Normalizes headers: 'Agente compra' -> 'agente_compra'.
    4. Type casting: decimal commas to dots, dates to objects.
    
    Returns:
        pd.DataFrame: Cleaned data or None if parsing fails.
    """
    try:
        text_content = content.decode('latin-1', errors='replace')
        lines = text_content.splitlines()
        
        # Skip first 2 metadata lines (L0, L1) and check header at L2
        if len(lines) < 3:
            return None
            
        csv_content = '\n'.join(lines[2:])
        
        df = pd.read_csv(io.StringIO(csv_content), sep=';', on_bad_lines='skip')
        
        # Normalize columns using Regex to handle NBSP or other whitespace
        # Replace 1 or more whitespace chars with _
        df.columns = [re.sub(r'\s+', '_', c.strip().lower()) for c in df.columns]
        
        # Check integrity
        required = ['fecha', 'contrato', 'precio', 'cantidad']
        if not all(col in df.columns for col in required):
            logger.warning(f"Missing columns in {filename}. Found: {df.columns}")
            return None
            
        df = df.dropna(how='all') 
        if 'unnamed' in df.columns[-1] or 'unnamed:_11' in df.columns: 
             # Drop last column if unnamed (trailing ;)
             if 'unnamed' in df.columns[-1]:
                 df = df.iloc[:, :-1]
             
        df['source_file'] = filename
        
        # Types
        for c in ['precio', 'cantidad']:
            if c in df.columns:
                if df[c].dtype == 'object':
                     df[c] = df[c].astype(str).str.replace(',', '.', regex=False)
                df[c] = pd.to_numeric(df[c], errors='coerce').fillna(0.0)

        # Dates
        df['fecha_str'] = df['fecha']
        df['fecha'] = pd.to_datetime(df['fecha_str'], format='%d/%m/%Y', errors='coerce').dt.date
        
        # Momento casacion
        if 'momento_casación' in df.columns:
            df.rename(columns={'momento_casación': 'momento_casacion'}, inplace=True)
            
        if 'momento_casacion' in df.columns:
             df['momento_casacion'] = pd.to_datetime(df['momento_casacion'], format='%d/%m/%Y %H:%M:%S', errors='coerce')
        
        # Text fields
        text_cols = ['contrato', 'agente_compra', 'unidad_compra', 'zona_compra', 'agente_venta', 'unidad_venta', 'zona_venta']
        for c in text_cols:
            if c in df.columns:
                df[c] = df[c].fillna('').astype(str)
            else:
                df[c] = ''

        if 'fecha_str' in df.columns:
            df.drop(columns=['fecha_str'], inplace=True)

        return df

    except Exception as e:
        logger.error(f"Error parsing {filename}: {e}")
        return None

def create_table_if_not_exists():
    ddl = """
    CREATE TABLE IF NOT EXISTS omie.trades (
        fecha DATE,
        contrato VARCHAR(100),
        agente_compra VARCHAR(50),
        unidad_compra VARCHAR(50),
        zona_compra VARCHAR(50),
        agente_venta VARCHAR(50),
        unidad_venta VARCHAR(50),
        zona_venta VARCHAR(50),
        precio DOUBLE PRECISION,
        cantidad DOUBLE PRECISION,
        momento_casacion TIMESTAMP,
        source_file TEXT,
        PRIMARY KEY (fecha, contrato, agente_compra, unidad_compra, agente_venta, unidad_venta, precio, cantidad, momento_casacion)
    );
    """
    try:
        engine = get_engine()
        with engine.begin() as conn:
            conn.execute(text("CREATE SCHEMA IF NOT EXISTS omie"))
            conn.execute(text(ddl))
            conn.execute(text("CREATE INDEX IF NOT EXISTS idx_trades_contrato ON omie.trades (contrato)"))
    except Exception as e:
        logger.error(f"Error creating table: {e}")

def process_trades(start_date: datetime, end_date: datetime):
    storage = StorageManager()
    db_manager = DatabaseManager()
    
    create_table_if_not_exists()
    
    current_date = start_date
    
    # Pre-fetch existing dates to skip
    existing_dates = db_manager.get_existing_dates("trades", "omie", start_date, end_date)
    
    while current_date <= end_date:
        if current_date in existing_dates:
            # logger.info(f"Skipping {current_date}: Already in DB") # Verbose
            current_date += timedelta(days=1)
            continue

        year = current_date.strftime("%Y")
        month = current_date.strftime("%m")
        date_str = current_date.strftime("%Y%m%d") 
        
        zip_filename = f"trades_{year}{month}.zip"
        zip_path = f"bronze/omie/trades/{year}/{zip_filename}"
        
        if storage.exists(zip_path):
            try:
                zip_bytes = storage.read(zip_path)
                with zipfile.ZipFile(io.BytesIO(zip_bytes)) as z:
                    target_file = f"trades_{date_str}.1"
                    
                    found_file = None
                    for n in z.namelist():
                        if target_file.lower() in n.lower():
                            found_file = n
                            break
                    
                    if found_file:
                        logger.info(f"Extracting {found_file} from {zip_filename}")
                        content = z.read(found_file)
                        df = parse_trades_content(content, found_file)
                        
                        if df is not None and not df.empty:
                            silver_path = f"silver/omie/trades/{year}/{month}/{date_str}.parquet"
                            storage.save(silver_path, df.to_parquet(index=False))
                            
                            pk = ['fecha', 'contrato', 'agente_compra', 'unidad_compra', 'agente_venta', 'unidad_venta', 'precio', 'cantidad', 'momento_casacion']
                            valid_pk = [c for c in pk if c in df.columns]
                            
                            if valid_pk:
                                df = df.drop_duplicates(subset=valid_pk)
                            
                            engine = get_engine()
                            with engine.begin() as conn:
                                conn.execute(text("DELETE FROM omie.trades WHERE fecha = :d"), {"d": current_date.date()})
                                
                            db_manager.bulk_insert_df(df, "trades", schema="omie", pk_cols=valid_pk)
                            logger.info(f"Processed trades for {date_str}")
                        else:
                            logger.warning(f"No valid data in {found_file}")
            except Exception as e:
                logger.error(f"Error processing {zip_path}: {e}")
        
        current_date += timedelta(days=1)
