import logging
import pandas as pd
from datetime import datetime, timedelta
import io
import zipfile
from src.common.filesystem import StorageManager
from src.common.database import DatabaseManager, get_engine
from sqlalchemy import text

logger = logging.getLogger(__name__)

def parse_marginalpdbc_content(content: bytes, filename: str) -> pd.DataFrame:
    """
    Parses the content of a marginalpdbc file.
    Format is typically:
    MARGINALPDBC;2025;07;08;1;...
    HEADER row...
    Data rows...
    
    We need to handle the fact that it uses ';' separator.
    """
    try:
        # Decode bytes
        text_content = content.decode('latin-1', errors='replace')
        
        # Read lines
        lines = text_content.splitlines()
        if not lines: return None
        
        # Filter metadata lines (e.g. starting with MARGINALPDBC;)
        # We want only lines that start with a number (Year)
        data_lines = [l for l in lines if l and l[0].isdigit()]
        
        if not data_lines:
            return None
            
        # Parse CSV without header
        # Format assumed: Year; Month; Day; Period; MarginalPT; MarginalES;
        df = pd.read_csv(io.StringIO('\n'.join(data_lines)), sep=';', header=None)
        
        # Assign columns by position
        # Expecting 6 relevant columns + potential trailing empty due to ; path
        # [0: anio, 1: mes, 2: dia, 3: periodo, 4: marginal_pt, 5: marginal_es]
        
        expected_cols = ['anio', 'mes', 'dia', 'periodo', 'marginal_pt', 'marginal_es']
        
        # Clean unnamed/empty columns
        df = df.dropna(axis=1, how='all')
        
        if len(df.columns) == 6:
            df.columns = expected_cols
        elif len(df.columns) >= 6:
            # Take first 6
            df = df.iloc[:, :6]
            df.columns = expected_cols
        else:
            logger.error(f"Unexpected column count in {filename}: {len(df.columns)}")
            return None
            
        # Add metadata
        df['source_file'] = filename
        
        # Convert types (User: I4, I2, I2, I3, F8.2, F8.2)
        df['anio'] = pd.to_numeric(df['anio'], errors='coerce').fillna(0).astype('int32')
        df['mes'] = pd.to_numeric(df['mes'], errors='coerce').fillna(0).astype('int32')
        df['dia'] = pd.to_numeric(df['dia'], errors='coerce').fillna(0).astype('int32')
        df['periodo'] = pd.to_numeric(df['periodo'], errors='coerce').fillna(0).astype('int32')
        
        # Handle decimals
        for col in ['marginal_pt', 'marginal_es']:
             if df[col].dtype == 'object':
                 df[col] = df[col].str.replace(',', '.', regex=False)
             df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # Add 'fecha' derived column as DATE
        df['fecha'] = pd.to_datetime(df[['anio', 'mes', 'dia']].rename(columns={'anio':'year', 'mes':'month', 'dia':'day'})).dt.date
        
        # Calculate 'resolucion'
        # Logic: "H" if 23, 24, or 25 periods. "QH" otherwise.
        # Since this function parses a single file (usually one day), we can check len(df) or max(periodo).
        # Checking len(df) is safer if there are missing periods, but max(periodo) is more semantic?
        # User said "si hay 23, 24 o 25 periodo", likely referring to the count of rows/periods in the day.
        row_count = len(df)
        if row_count in [23, 24, 25]:
            df['resolucion'] = 'H'
        else:
            df['resolucion'] = 'QH'
            
        return df
        
    except Exception as e:
        logger.error(f"Error parsing content of {filename}: {e}")
        return None
        
    except Exception as e:
        logger.error(f"Error parsing content of {filename}: {e}")
        return None

def create_table_if_not_exists():
    """
    Creates the omie.marginalpdbc table with strict schema if it doesn't exist.
    """
    ddl = """
    CREATE TABLE IF NOT EXISTS omie.marginalpdbc (
        anio INTEGER,
        mes INTEGER,
        dia INTEGER,
        periodo INTEGER,
        marginal_pt DOUBLE PRECISION,
        marginal_es DOUBLE PRECISION,
        source_file TEXT,
        fecha DATE,
        resolucion VARCHAR(5),
        PRIMARY KEY (anio, mes, dia, periodo)
    );
    """
    try:
        engine = get_engine()
        with engine.begin() as conn:
            conn.execute(text("CREATE SCHEMA IF NOT EXISTS omie"))
            conn.execute(text(ddl))
            logger.info("Ensured table omie.marginalpdbc exists.")
    except Exception as e:
        logger.error(f"Error creating table: {e}")

def process_marginalpdbc(start_date: datetime, end_date: datetime):
    """
    Process marginalpdbc files (Bronze -> Silver -> DB).
    """
    storage = StorageManager()
    db_manager = DatabaseManager()
    
    # Ensure strict schema
    create_table_if_not_exists()
    
    current_date = start_date
    existing_dates = db_manager.get_existing_dates("marginalpdbc", "omie", start_date, end_date)

    while current_date <= end_date:

        year = current_date.strftime("%Y")
        month = current_date.strftime("%m")
        today_str = current_date.strftime("%Y%m%d")
        
        # 1. Identify Source File in Bronze
        # Could be a ZIP (annual) or a daily file (.1)
        
        # Check Daily first (post-2023)
        daily_path = f"bronze/omie/marginalpdbc/{year}/{month}/marginalpdbc_{today_str}.1"
        zip_path = f"bronze/omie/marginalpdbc/{year}/marginalpdbc_{year}.zip"
        
        files_to_process = [] # list of (filename, content_bytes)
        
        if storage.exists(daily_path):
            content = storage.read(daily_path)
            files_to_process.append((f"marginalpdbc_{today_str}.1", content))
            
        elif storage.exists(zip_path):
            # Extract specific day from zip? 
            # Or if it's an annual zip, processing it day-by-day is inefficient if we re-read the zip 365 times.
            # But the 'process' command usually runs for a range.
            # For efficiency, if range covers full year, we process zip once.
            # But here we loop day by day. 
            # Optimization: Cache zip content or extracted list? 
            # For now, let's just read the zip and find the specific file for *this* day.
            
            zip_content = storage.read(zip_path)
            try:
                with zipfile.ZipFile(io.BytesIO(zip_content)) as z:
                    # Find file inside zip matching date
                    # Zip contents usually: marginalpdbc_YYYYMMDD.1
                    target_name = f"marginalpdbc_{today_str}.1"
                    # Case insensitive search
                    found_name = None
                    for n in z.namelist():
                        if target_name.lower() in n.lower():
                            found_name = n
                            break
                    
                    if found_name:
                        files_to_process.append((found_name, z.read(found_name)))
            except Exception as e:
                logger.error(f"Error reading zip {zip_path}: {e}")

        # 2. Process Files
        for fname, content in files_to_process:
            logger.info(f"Processing Silver for {fname}...")
            
            df = parse_marginalpdbc_content(content, fname)
            if df is not None and not df.empty:
                # Save Parquet
                silver_path = f"silver/omie/marginalpdbc/{year}/{month}/{today_str}_{fname}.parquet"
                storage.save(silver_path, df.to_parquet(index=False))
                
                # DB Ingest
                # Schema: omie, Table: marginalpdbc
                # PK: anio, mes, dia, periodo
                pk = ['anio', 'mes', 'dia', 'periodo']
                
                # Verify we have these columns
                if set(pk).issubset(df.columns):
                    df.drop_duplicates(subset=pk, keep='last', inplace=True)
                    
                    try:
                        # Idempotency: Delete existing records for this day (anio, mes, dia)
                        # We assume the file covers one day or few days.
                        unique_days = df[['anio', 'mes', 'dia']].drop_duplicates()
                        engine = get_engine()
                        with engine.begin() as conn:
                            for _, row in unique_days.iterrows():
                                # Safe delete
                                query = text(f"DELETE FROM omie.marginalpdbc WHERE anio=:anio AND mes=:mes AND dia=:dia")
                                conn.execute(query, {"anio": int(row['anio']), "mes": int(row['mes']), "dia": int(row['dia'])})
                                logger.info(f"Deleted existing rows for {row['anio']}-{row['mes']}-{row['dia']} to allow overwrite.")
                        
                        db_manager.bulk_insert_df(df, "marginalpdbc", schema="omie", pk_cols=pk)
                        db_manager.create_indexes("marginalpdbc", ['anio', 'mes', 'dia'], schema="omie")
                        
                    except Exception as e:
                        logger.error(f"Error ingesting {fname}: {e}")
                        # User requested to continue processing if error occurs
                        pass
                        
                else:
                    logger.warning(f"Could not determine PK for {fname}. Inserting without dedup.")
                    try:
                        db_manager.bulk_insert_df(df, "marginalpdbc", schema="omie")
                    except Exception as e:
                        logger.error(f"Error ingesting (no-pk) {fname}: {e}")
                        pass
                    
        current_date += timedelta(days=1)
