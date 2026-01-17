import pandas as pd
from sqlalchemy import text, create_engine
import logging
from io import StringIO
from src.config.settings import DATABASE_URL

logger = logging.getLogger(__name__)

# Global engine instance
_engine = None

def get_engine():
    global _engine
    if _engine is None:
        _engine = create_engine(DATABASE_URL, pool_pre_ping=True)
    return _engine

class DatabaseManager:
    """
    Optimized manager for table operations and bulk insertion.
    """

    @staticmethod
    def drop_schema_tables(schema: str):
        """
        Deletes all tables in the specified schema.
        """
        engine = get_engine()
        with engine.begin() as conn:
            # Get all table names in the schema
            query = text("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = :schema
            """)
            tables = conn.execute(query, {"schema": schema}).fetchall()
            
            for table in tables:
                table_name = table[0]
                conn.execute(text(f"DROP TABLE IF EXISTS {schema}.\"{table_name}\" CASCADE"))
                logger.info(f"Dropped table {schema}.{table_name}")

    @staticmethod
    def create_table_if_not_exists(table_name: str, schema: str, columns: dict, pk_cols: list[str] = None):
        """
        Creates a table strictly based on the schema dictionary if it doesn't exist.
        columns: dict { 'col_name': 'SQL_TYPE' }
        pk_cols: list of columns that form the Primary Key. If None, defaults to 'id' SERIAL.
        """
        engine = get_engine()
        table_name = table_name.lower()
        full_table_name = f"{schema}.\"{table_name}\""
        
        # Work on a copy to avoid side effects
        columns = columns.copy()
        
        # Add standard metadata columns if missing
        if 'source_file' not in columns:
            columns['source_file'] = 'TEXT'
        if 'fecha_proceso' not in columns:
            columns['fecha_proceso'] = 'DATE'
        if 'resolucion' not in columns:
            columns['resolucion'] = 'VARCHAR(5)'
        if 'liquidacion' not in columns:
            columns['liquidacion'] = 'VARCHAR(10)'
            
        # Logic for ID vs Custom PK
        if not pk_cols:
            if 'id' not in columns:
                columns['id'] = 'SERIAL PRIMARY KEY'
        
        col_defs = []
        for col, dtype in columns.items():
            if not pk_cols and col == 'id' and 'PRIMARY KEY' not in dtype:
                 dtype += ' PRIMARY KEY'
            col_defs.append(f"\"{col}\" {dtype}")
            
        if pk_cols:
             pk_str = ", ".join([f"\"{c}\"" for c in pk_cols])
             col_defs.append(f"PRIMARY KEY ({pk_str})")
            
        create_sql = f"CREATE TABLE IF NOT EXISTS {full_table_name} ({', '.join(col_defs)})"
        
        with engine.begin() as conn:
            try:
                conn.execute(text(f"CREATE SCHEMA IF NOT EXISTS {schema}"))
                conn.execute(text(create_sql))
                logger.info(f"Table {full_table_name} ensured.")
            except Exception as e:
                logger.error(f"Error creating table {full_table_name}: {e}")
                raise

    @staticmethod
    def safe_drop_table(table_name: str, schema: str):
        """
        Drops a single table if it exists.
        """
        engine = get_engine()
        try:
            with engine.begin() as conn:
                conn.execute(text(f"DROP TABLE IF EXISTS {schema}.\"{table_name}\" CASCADE"))
                logger.info(f"Dropped table {schema}.{table_name}")
        except Exception as e:
            logger.warning(f"Error dropping table {schema}.{table_name}: {e}")

    @staticmethod
    def bulk_insert_df(df: pd.DataFrame, table_name: str, schema: str = 'public', if_exists: str = 'append', pk_cols: list[str] = None):
        """
        Inserts a DataFrame into PostgreSQL using the COPY command for maximum speed.
        """
        engine = get_engine()
        
        # Clean table name
        table_name = table_name.lower().replace(" ", "_").replace("-", "_").replace(".", "")
        full_table_name = f"{schema}.{table_name}"

        # 0. Handle nulls in PK columns
        # Logic removed to avoid corrupting DATE/Time columns with 'N/A'.
        # Caller is responsible for ensuring PKs are valid (not null).
        # if pk_cols:
        #     for col in pk_cols:
        #         if col in df.columns:
        #             if pd.api.types.is_numeric_dtype(df[col]):
        #                 df[col] = df[col].fillna(0)
        #             else:
        #                 df[col] = df[col].fillna('N/A')
        #                 if hasattr(df[col], 'str'):
        #                     df[col] = df[col].replace('', 'N/A')
        
        with engine.begin() as conn:
            # Check if table exists in the specific schema
            exists_query = text("SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_schema = :schema AND table_name = :table)")
            exists = conn.execute(exists_query, {"schema": schema, "table": table_name}).scalar()
            
            if not exists or if_exists == 'replace':
                # Use pandas to create the table structure first
                df.head(0).to_sql(table_name, conn, schema=schema, if_exists='replace', index=False)
                
                # Add Primary Key if provided
                if pk_cols:
                    pk_str = ", ".join([f"\"{c}\"" for c in pk_cols])
                    try:
                        conn.execute(text(f"ALTER TABLE {schema}.\"{table_name}\" ADD PRIMARY KEY ({pk_str})"))
                        logger.info(f"Primary Key ({pk_str}) added to '{full_table_name}'.")
                    except Exception as e:
                        logger.warning(f"Could not add PK to {full_table_name}: {e}")
                
                logger.info(f"Table '{full_table_name}' created/replaced.")
            
            if if_exists == 'fail' and exists:
                raise ValueError(f"Table {full_table_name} already exists.")

        # Prepare for COPY
        raw_conn = engine.raw_connection()
        try:
            with raw_conn.cursor() as cur:
                output = StringIO()
                NULL_MARKER = '__NULL__'
                df.to_csv(output, sep='\t', header=False, index=False, na_rep=NULL_MARKER)
                output.seek(0)
                
                columns = ', '.join([f'"{c}"' for c in df.columns])
                sql = f"COPY {full_table_name} ({columns}) FROM STDIN WITH CSV DELIMITER '\t' NULL '{NULL_MARKER}'"
                cur.copy_expert(sql, output)
                raw_conn.commit()
                logger.info(f"Inserted {len(df)} rows into '{full_table_name}'.")
        except Exception as e:
            raw_conn.rollback()
            logger.error(f"Error during bulk insert into {full_table_name}: {e}")
            raise
        finally:
            raw_conn.close()

    @staticmethod
    def create_indexes(table_name: str, columns: list[str], schema: str = 'public'):
        """
        Creates B-Tree indexes for specified columns to optimize read speed.
        """
        engine = get_engine()
        table_name = table_name.lower()
        full_table_name = f"{schema}.\"{table_name}\""
        
        with engine.begin() as conn:
            for col in columns:
                index_name = f"idx_{table_name}_{col}"
                try:
                    conn.execute(text(f"CREATE INDEX IF NOT EXISTS \"{index_name}\" ON {full_table_name} (\"{col}\")"))
                    logger.info(f"Index '{index_name}' checked/created on {full_table_name}.")
                except Exception as e:
                    logger.warning(f"Could not create index on {col} in {full_table_name}: {e}")

    @staticmethod
    def drop_indexes(table_name: str, columns: list[str], schema: str = 'public'):
        """
        Drops indexes for specified columns to optimize write speed during bulk inserts.
        """
        engine = get_engine()
        table_name = table_name.lower()
        full_table_name = f"{schema}.\"{table_name}\""
        
        with engine.begin() as conn:
            for col in columns:
                index_name = f"idx_{table_name}_{col}"
                try:
                    conn.execute(text(f"DROP INDEX IF EXISTS {schema}.\"{index_name}\""))
                    logger.info(f"Index '{index_name}' dropped from {full_table_name}.")
                except Exception as e:
                    logger.warning(f"Could not drop index {index_name} on {full_table_name}: {e}")
