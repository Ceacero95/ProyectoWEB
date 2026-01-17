
import logging
from datetime import datetime
from src.silver.liquicomun_parquet import ingest_to_parquet
from src.silver.liquicomun import process_liquicomun

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("history_load.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("HistoryLoader")

def main():
    start_date = datetime(2025, 1, 1)
    end_date = datetime(2026, 1, 17) # Adjust as needed based on actual max date
    
    logger.info(f"Starting historical load from {start_date.date()} to {end_date.date()}")
    
    try:
        logger.info(">>> STEP 1: Bronze -> Silver (Parquet) <<<")
        ingest_to_parquet(start_date, end_date)
        
        logger.info(">>> STEP 2: Silver -> Gold (Database) <<<")
        process_liquicomun(start_date, end_date)
        
        logger.info("Historical load completed successfully.")
        
    except Exception as e:
        logger.error(f"Historical load failed: {e}")
        raise

if __name__ == "__main__":
    main()
