import logging
import pandas as pd
from datetime import datetime, timedelta
import io
from src.common.filesystem import StorageManager
from src.common.database import DatabaseManager, get_engine
from sqlalchemy import text

logger = logging.getLogger(__name__)

def parse_marginalpibc_content(content: bytes, filename: str) -> pd.DataFrame:
    """
    Parses marginalpibc content.
    Similar to pdbc but extracts 'mercado' from filename extension/suffix.
    """
    try:
        text_content = content.decode('latin-1', errors='replace')
        lines = text_content.splitlines()
        
        # Filter metadata, keep data lines
        data_lines = [l for l in lines if l and l[0].isdigit()]
        
        if not data_lines:
            return None
            
        # Parse CSV without header
        # Expected cols: Year; Month; Day; Period; PricePT; PriceES; (maybe Block? Usually just Prices)
        # Check actual columns dynamically if possible, or assume 6 like pdbc
        df = pd.read_csv(io.StringIO('\n'.join(data_lines)), sep=';', header=None)
        
        # Drop empty cols
        df = df.dropna(axis=1, how='all')
        
        # Expected: anio, mes, dia, periodo, marginal_pt, marginal_es
        # Wait, usually for Intraday, columns are same? 
        # Let's assume yes based on "marginal" name.
        expected_cols = ['anio', 'mes', 'dia', 'periodo', 'marginal_pt', 'marginal_es']
        
        if len(df.columns) >= 6:
             df = df.iloc[:, :6]
             df.columns = expected_cols
        else:
            logger.warning(f"Unexpected columns in {filename}: {len(df.columns)}")
            return None
            
        # Metadata
        df['source_file'] = filename
        
        # Extract 'mercado' from filename extension/suffix
        # filename format: marginalpibc_YYYYMMDDMM.1 (e.g. ...01.1 -> mercado 1)
        try:
            import re
            # Match 2 digits before .1
            match = re.search(r'(\d{2})\.1$', filename)
            if match:
                df['mercado'] = int(match.group(1))
            else:
                 # Fallback
                df['mercado'] = 0
        except:
             df['mercado'] = 0

        # Types
        for c in ['anio', 'mes', 'dia', 'periodo', 'mercado']:
            df[c] = pd.to_numeric(df[c], errors='coerce').fillna(0).astype('int32')
            
        for c in ['marginal_pt', 'marginal_es']:
            if df[c].dtype == 'object':
                 df[c] = df[c].str.replace(',', '.', regex=False)
            df[c] = pd.to_numeric(df[c], errors='coerce')

        # Derived cols
        df['fecha'] = pd.to_datetime(df[['anio', 'mes', 'dia']].rename(columns={'anio':'year', 'mes':'month', 'dia':'day'})).dt.date
        
        # Resolucion
        row_count = len(df)
        if row_count in [23, 24, 25]:
            df['resolucion'] = 'H'
        else:
            df['resolucion'] = 'QH'
            
        return df
        
    except Exception as e:
        logger.error(f"Error parsing {filename}: {e}")
        return None

def create_table_if_not_exists():
    ddl = """
    CREATE TABLE IF NOT EXISTS omie.marginalpibc (
        anio INTEGER,
        mes INTEGER,
        dia INTEGER,
        periodo INTEGER,
        marginal_pt DOUBLE PRECISION,
        marginal_es DOUBLE PRECISION,
        mercado INTEGER,
        source_file TEXT,
        fecha DATE,
        resolucion VARCHAR(5),
        PRIMARY KEY (anio, mes, dia, periodo, mercado)
    );
    """
    try:
        engine = get_engine()
        with engine.begin() as conn:
            conn.execute(text("CREATE SCHEMA IF NOT EXISTS omie"))
            conn.execute(text(ddl))
            logger.info("Ensured table omie.marginalpibc exists.")
    except Exception as e:
        logger.error(f"Error creating table: {e}")

def process_marginalpibc(start_date: datetime, end_date: datetime):
    storage = StorageManager()
    db_manager = DatabaseManager()
    
    create_table_if_not_exists()
    
    current_date = start_date
    existing_dates = db_manager.get_existing_dates("marginalpibc", "omie", start_date, end_date)

    while current_date <= end_date:

        year = current_date.strftime("%Y")
        month = current_date.strftime("%m")
        date_str = current_date.strftime("%Y%m%d")
        
        # Look for files in Bronze (1..7)
        # We can list files or iterate. Iterating is safer for predictable patterns.
        # But `list_files` would be better if we don't know exact counts.
        # StorageManager has list_files? Yes (if implemented local).
        # Let's try iterating 1..10 to be safe.
        
        files_to_process = []
        for i in range(1, 4):
            # Filename format: marginalpibc_YYYYMMDDMM.1
            fname = f"marginalpibc_{date_str}{i:02d}.1"
            path = f"bronze/omie/marginalpibc/{year}/{month}/{fname}"
            
            if storage.exists(path):
                files_to_process.append((fname, storage.read(path)))
        
        for fname, content in files_to_process:
            logger.info(f"Processing Silver {fname}...")
            df = parse_marginalpibc_content(content, fname)
            
            if df is not None and not df.empty:
                # Save Parquet
                # Ensure date format is plain YYYY-MM-DD string
                df_parquet = df.copy()
                df_parquet['fecha'] = df_parquet['fecha'].astype(str)

                silver_path = f"silver/omie/marginalpibc/{year}/{month}/{date_str}_{fname}.parquet"
                storage.save(silver_path, df_parquet.to_parquet(index=False))
                
                # Ingest
                pk = ['anio', 'mes', 'dia', 'periodo', 'mercado']
                
                if set(pk).issubset(df.columns):
                    df.drop_duplicates(subset=pk, keep='last', inplace=True)
                    
                    try:
                        # Idempotency & Atomicity: Delete and Insert in SAME transaction
                        mercado = df['mercado'].iloc[0] # assume 1 file = 1 market
                        engine = get_engine()
                        with engine.begin() as conn:
                             # 1. Delete
                             q = text("DELETE FROM omie.marginalpibc WHERE anio=:y AND mes=:m AND dia=:d AND mercado=:mk")
                             conn.execute(q, {"y": int(df['anio'].iloc[0]), "m": int(df['mes'].iloc[0]), "d": int(df['dia'].iloc[0]), "mk": int(mercado)})
                             
                             # 2. Insert
                             df.to_sql("marginalpibc", conn, schema="omie", if_exists='append', index=False)
                        
                        logger.info(f"Successfully processed {fname}")
                        
                    except Exception as e:
                        logger.error(f"Error ingesting {fname}: {e}")
                        pass
                else:
                    logger.warning(f"PK missing in {fname}")
        
        current_date += timedelta(days=1)
