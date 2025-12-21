import psycopg2
from src.config.settings import DB_CONFIG

class DBConnector:
    def __init__(self):
        self._conn = None
    def __enter__(self):
        try:
            self._conn = psycopg2.connect(**DB_CONFIG)
            return self._conn
        except psycopg2.Error as e:
            print(f"Error DB: {e}")
            raise
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._conn:
            self._conn.close()

def execute_query(query, params=None, fetch_results=False):
    with DBConnector() as conn:
        with conn.cursor() as cur:
            cur.execute(query, params)
            if fetch_results:
                return cur.fetchall()
            else:
                conn.commit()
                return None
