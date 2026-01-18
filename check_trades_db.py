
from src.common.database import get_engine
from sqlalchemy import text

def check_db():
    engine = get_engine()
    with engine.connect() as conn:
        result = conn.execute(text("SELECT count(*) FROM omie.trades WHERE fecha = '2025-10-01'"))
        count = result.scalar()
        print(f"Rows in omie.trades for 2025-10-01: {count}")
        
        # Show sample
        if count > 0:
            sample = conn.execute(text("SELECT agente_compra, unidad_compra, precio FROM omie.trades WHERE fecha = '2025-10-01' LIMIT 1")).fetchone()
            print("Sample data:", sample)

if __name__ == "__main__":
    check_db()
