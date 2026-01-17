import logging
import sys
import os
from sqlalchemy import text

sys.path.append(os.getcwd())
from src.common.database import DatabaseManager, get_engine

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("cleanup")

def clean_database():
    schemas = ['i90', 'i3', 'liquicomun']
    engine = get_engine()
    
    with engine.begin() as conn:
        for schema in schemas:
            logger.info(f"Cleaning schema: {schema}")
            try:
                # Check if schema exists
                exists = conn.execute(text(f"SELECT 1 FROM information_schema.schemata WHERE schema_name = '{schema}'")).scalar()
                if exists:
                    # Drop tables
                    DatabaseManager.drop_schema_tables(schema)
                else:
                    logger.info(f"Schema {schema} does not exist.")
            except Exception as e:
                logger.error(f"Error cleaning {schema}: {e}")

if __name__ == "__main__":
    clean_database()
