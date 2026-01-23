import sys
from sqlalchemy import text
sys.path.append("/opt/airflow")
from src.common.database import get_engine

def test_insert_manual():
    engine = get_engine()
    print("Connecting to DB...")
    
    # 1. Insert
    with engine.begin() as conn:
        print("Inserting test row for 2030-01-01...")
        query = text("""
            INSERT INTO omie.marginalpdbc (anio, mes, dia, periodo, marginal_pt, marginal_es, fecha, resolucion, source_file)
            VALUES (2030, 1, 1, 1, 99.99, 99.99, '2030-01-01', 'H', 'TEST_MANUAL')
            ON CONFLICT (anio, mes, dia, periodo) DO NOTHING
        """)
        conn.execute(query)
        print("Insert executed.")

    # 2. Select back
    with engine.connect() as conn:
        print("Selecting back...")
        result = conn.execute(text("SELECT * FROM omie.marginalpdbc WHERE anio=2030 AND mes=1 AND dia=1")).fetchall()
        print(f"Result matching 2030-01-01: {result}")

if __name__ == "__main__":
    test_insert_manual()
