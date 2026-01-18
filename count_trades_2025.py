
from src.common.database import get_engine
from sqlalchemy import text

def count_2025():
    engine = get_engine()
    with engine.connect() as conn:
        result = conn.execute(text("SELECT count(*) FROM omie.trades WHERE fecha >= '2025-01-01' AND fecha <= '2025-12-31'"))
        count = result.scalar()
        print(f"Total Trades rows for 2025: {count}")

if __name__ == "__main__":
    count_2025()
