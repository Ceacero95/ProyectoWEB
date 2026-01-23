import sys
from datetime import datetime, timedelta
sys.path.append("/opt/airflow")
from src.common.database import get_engine
from sqlalchemy import text

def check_latest_dates():
    engine = get_engine()
    tables = ["marginalpdbc", "marginalpibc"]
    
    with engine.connect() as conn:
        print("\n--- FECHAS MÁXIMAS EN BBDD ---")
        for t in tables:
            try:
                # Obtener la fecha máxima real registrada
                query = text(f"SELECT MAX(fecha) FROM omie.{t}")
                result = conn.execute(query).scalar()
                print(f"{t}: {result}")
                
                # Obtener conteo de los últimos 5 días
                if result:
                    limit_date = result - timedelta(days=5)
                    q2 = text(f"SELECT fecha, count(*) FROM omie.{t} WHERE fecha >= :d GROUP BY fecha ORDER BY fecha DESC")
                    rows = conn.execute(q2, {"d": limit_date}).fetchall()
                    for r in rows:
                        print(f"   -> {r[0]}: {r[1]} registros")
            except Exception as e:
                print(f"{t}: Error {e}")

if __name__ == "__main__":
    check_latest_dates()
