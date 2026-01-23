import logging
import pandas as pd
from datetime import datetime, timedelta
import io
import zipfile
from sqlalchemy import text
from src.common.filesystem import StorageManager
from src.common.database import DatabaseManager, get_engine

logger = logging.getLogger(__name__)

def parse_pdbc_content(content: bytes, filename: str) -> pd.DataFrame:
    try:
        text_content = content.decode('latin-1', errors='replace')
        lines = text_content.splitlines()
        data_lines = [l for l in lines if l and l[0].isdigit()]
        
        if not data_lines: return None
        
        df = pd.read_csv(io.StringIO('\n'.join(data_lines)), sep=';', header=None)
        
        # PDBC spec: Anio;Mes;Dia;Periodo;UOF;Energia;Precio;Tipo;Oferta
        expected_cols = ['anio', 'mes', 'dia', 'periodo', 'codigo_uof', 'energia', 'precio', 'tipo_oferta', 'codigo_oferta']
        
        if len(df.columns) >= 9:
            df = df.iloc[:, :9]
            df.columns = expected_cols
        else:
            logger.warning(f"Unexpected columns in {filename}: {len(df.columns)}")
            return None
            
        df['source_file'] = filename
        
        # Types
        int_cols = ['anio', 'mes', 'dia', 'periodo']
        for c in int_cols:
            df[c] = pd.to_numeric(df[c], errors='coerce').fillna(0).astype('int32')

        float_cols = ['energia', 'precio']
        for c in float_cols:
             if df[c].dtype == 'object':
                 df[c] = df[c].str.replace(',', '.', regex=False)
             df[c] = pd.to_numeric(df[c], errors='coerce')

        # codigo_uof is text
        # tipo_oferta usually int (1), codigo_oferta int/long
        df['tipo_oferta'] = pd.to_numeric(df['tipo_oferta'], errors='coerce').fillna(0).astype('int32')
        # codigo_oferta might be large, keep as float/text or numeric?
        # sample: 9999453 -> int
        df['codigo_oferta'] = pd.to_numeric(df['codigo_oferta'], errors='coerce').fillna(0).astype('int64')

        df['fecha'] = pd.to_datetime(df[['anio', 'mes', 'dia']].rename(columns={'anio':'year', 'mes':'month', 'dia':'day'})).dt.date
        
        if len(df) <= 25: # Rough check, but this is huge file, header check is per file?
            # Wait, PDBC is by unit. Rows >> 24.
            # Resolucion relies on row count OF PERIODS?
            # No, every row has a period.
            # We assume QH if Period goes > 25?
            # Max(periodo)
            df['resolucion'] = 'QH' if df['periodo'].max() > 25 else 'H'
        else:
             df['resolucion'] = 'QH' if df['periodo'].max() > 25 else 'H'
            
        return df

    except Exception as e:
        logger.error(f"Error parsing {filename}: {e}")
        return None

def create_table_if_not_exists():
    ddl = """
    CREATE TABLE IF NOT EXISTS omie.pdbc (
        anio INTEGER,
        mes INTEGER,
        dia INTEGER,
        periodo INTEGER,
        codigo_uof VARCHAR(50),
        energia DOUBLE PRECISION,
        precio DOUBLE PRECISION,
        tipo_oferta INTEGER,
        codigo_oferta BIGINT,
        source_file TEXT,
        fecha DATE,
        resolucion VARCHAR(5),
        PRIMARY KEY (anio, mes, dia, periodo, codigo_uof, codigo_oferta)
    );
    """
    # Note: PK might need to include codigo_oferta? Or UOF?
    # A unit can have multiple offers?
    # Sample has UOF repeated? No, ABA1, ABA2.
    # UOF is likely unique per period?
    # But wait, same UOF?
    # I'll include 'codigo_uof' and 'codigo_oferta' in PK to be safe.
    try:
        engine = get_engine()
        with engine.begin() as conn:
            conn.execute(text("CREATE SCHEMA IF NOT EXISTS omie"))
            conn.execute(text(ddl))
            # conn.execute(text("CREATE INDEX IF NOT EXISTS idx_pdbc_fecha ON omie.pdbc (fecha)"))
    except Exception as e:
        logger.error(f"Error creating table: {e}")

def process_pdbc(start_date: datetime, end_date: datetime):
    storage = StorageManager()
    db_manager = DatabaseManager()
    
    current_date = start_date
    existing_dates = db_manager.get_existing_dates("pdbc", "omie", start_date, end_date)
    
    while current_date <= end_date:
        if current_date in existing_dates:
            current_date += timedelta(days=1)
            continue

        year = current_date.strftime("%Y")
        month = current_date.strftime("%m")
        date_str = current_date.strftime("%Y%m%d")
        
        # Bronze is Monthly ZIP: pdbc_YYYYMM.zip
        zip_filename = f"pdbc_{year}{month}.zip"
        zip_path = f"bronze/omie/pdbc/{year}/{zip_filename}"
        
        if storage.exists(zip_path):
            try:
                zip_bytes = storage.read(zip_path)
                with zipfile.ZipFile(io.BytesIO(zip_bytes)) as z:
                    # Look for daily file: pdbc_YYYYMMDD.1 ?
                    # Or just match date in name.
                    target_stub = f"pdbc_{date_str}"
                    found_file = None
                    for n in z.namelist():
                        if target_stub in n.lower():
                            found_file = n
                            break
                    
                    if found_file:
                        content = z.read(found_file)
                        df = parse_pdbc_content(content, found_file)
                        
                        if df is not None and not df.empty:
                            create_table_if_not_exists()
                            
                            # Save Parquet
                            silver_path = f"silver/omie/pdbc/{year}/{month}/{date_str}.parquet"
                            storage.save(silver_path, df.to_parquet(index=False))
                            
                            # Ingest
                            pk = ['anio', 'mes', 'dia', 'periodo', 'codigo_uof', 'codigo_oferta']

                            # Deduplicate
                            if set(pk).issubset(df.columns):
                                df = df.drop_duplicates(subset=pk, keep='last')
                            
                            # Delete existing
                            engine = get_engine()
                            with engine.begin() as conn:
                                conn.execute(text("DELETE FROM omie.pdbc WHERE fecha = :d"), {"d": current_date.date()})
                                
                            db_manager.bulk_insert_df(df, "pdbc", schema="omie", pk_cols=pk)
                            logger.info(f"Processed pdbc for {date_str}")
            except Exception as e:
                logger.error(f"Error processing zip {zip_path}: {e}")
        
        current_date += timedelta(days=1)
