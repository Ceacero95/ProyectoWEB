import logging
import pandas as pd
from datetime import datetime, timedelta
import io
import zipfile
from sqlalchemy import text
from src.common.filesystem import StorageManager
from src.common.database import DatabaseManager, get_engine

logger = logging.getLogger(__name__)

def parse_pdbf_content(content: bytes, filename: str) -> pd.DataFrame:
    try:
        text_content = content.decode('latin-1', errors='replace')
        lines = text_content.splitlines()
        data_lines = [l for l in lines if l and l[0].isdigit()]
        
        if not data_lines: return None
        
        df = pd.read_csv(io.StringIO('\n'.join(data_lines)), sep=';', header=None)
        
        # PDBF spec: Anio;Mes;Dia;Periodo;UOF;Energia;Precio(empty);Tipo;Oferta
        expected_cols = ['anio', 'mes', 'dia', 'periodo', 'codigo_uof', 'energia', 'precio', 'tipo_oferta', 'codigo_oferta']
        
        if len(df.columns) >= 9:
            df = df.iloc[:, :9]
            df.columns = expected_cols
        else:
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

        df['tipo_oferta'] = pd.to_numeric(df['tipo_oferta'], errors='coerce').fillna(0).astype('int32')
        df['codigo_oferta'] = pd.to_numeric(df['codigo_oferta'], errors='coerce').fillna(0).astype('int64')

        df['fecha'] = pd.to_datetime(df[['anio', 'mes', 'dia']].rename(columns={'anio':'year', 'mes':'month', 'dia':'day'})).dt.date
        df['resolucion'] = 'QH' if df['periodo'].max() > 25 else 'H'
            
        return df

    except Exception as e:
        logger.error(f"Error parsing {filename}: {e}")
        return None

def create_table_if_not_exists():
    ddl = """
    CREATE TABLE IF NOT EXISTS omie.pdbf (
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
    try:
        engine = get_engine()
        with engine.begin() as conn:
            conn.execute(text(ddl))
    except Exception as e:
        logger.error(f"Error creating table: {e}")

def process_pdbf(start_date: datetime, end_date: datetime):
    storage = StorageManager()
    db_manager = DatabaseManager()
    
    current_date = start_date
    while current_date <= end_date:
        year = current_date.strftime("%Y")
        month = current_date.strftime("%m")
        date_str = current_date.strftime("%Y%m%d")
        
        zip_filename = f"pdbf_{year}{month}.zip"
        zip_path = f"bronze/omie/pdbf/{year}/{zip_filename}"
        
        if storage.exists(zip_path):
            try:
                zip_bytes = storage.read(zip_path)
                with zipfile.ZipFile(io.BytesIO(zip_bytes)) as z:
                    target_stub = f"pdbf_{date_str}"
                    found_file = None
                    for n in z.namelist():
                        if target_stub in n.lower():
                            found_file = n
                            break
                    
                    if found_file:
                        content = z.read(found_file)
                        df = parse_pdbf_content(content, found_file)
                        
                        if df is not None and not df.empty:
                            create_table_if_not_exists()
                            
                            silver_path = f"silver/omie/pdbf/{year}/{month}/{date_str}.parquet"
                            storage.save(silver_path, df.to_parquet(index=False))
                            
                            pk = ['anio', 'mes', 'dia', 'periodo', 'codigo_uof', 'codigo_oferta']
                            
                            if set(pk).issubset(df.columns):
                                df = df.drop_duplicates(subset=pk, keep='last')
                            
                            engine = get_engine()
                            with engine.begin() as conn:
                                conn.execute(text("DELETE FROM omie.pdbf WHERE fecha = :d"), {"d": current_date.date()})
                                
                            db_manager.bulk_insert_df(df, "pdbf", schema="omie", pk_cols=pk)
                            logger.info(f"Processed pdbf for {date_str}")
            except Exception as e:
                logger.error(f"Error processing zip {zip_path}: {e}")
        
        current_date += timedelta(days=1)
