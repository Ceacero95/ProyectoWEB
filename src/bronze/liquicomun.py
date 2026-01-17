import logging
import argparse
from datetime import datetime, timedelta
from src.common.client import EsiosClient
from src.common.filesystem import StorageManager
from src.config import settings

logger = logging.getLogger(__name__)

def download_liquicomun(start_date: datetime, end_date: datetime):
    """
    Downloads Liquicomun files for the specified date range.
    """
    client = EsiosClient()
    storage = StorageManager()
    
    current_date = start_date
    while current_date <= end_date:
        # Loop through all configured Liquicomun IDs
        for archive_id in settings.ESIOS_LIQUICOMUN_IDS:
            is_daily = archive_id in settings.ESIOS_LIQUICOMUN_DAILY_IDS
            
            # Predict filename and path
            year = current_date.strftime("%Y")
            month = current_date.strftime("%m")
            date_str = current_date.strftime("%Y%m%d")
            filename = f"esios_{archive_id}_{date_str}.zip"
            path = f"bronze/liquicomun/{year}/{month}/{filename}"
            
            # Conditional Download Logic
            if not is_daily:
                if storage.exists(path):
                    logger.info(f"Skipping {archive_id} for {current_date.date()} (Exists: {filename})")
                    continue
            
            logger.info(f"Checking/Downloading Liquicomun ID {archive_id} for {current_date.date()}...")
            
            try:
                # We already predicted the name, but client returns it too.
                # In strict refactor we might pass the name, but let's keep it simple.
                downloaded_name, content = client.download_archive(archive_id, current_date)
                
                if content:
                    # Verify name matches expectation (sanity check)
                    if downloaded_name != filename:
                        logger.warning(f"Downloaded name {downloaded_name} differs from expected {filename}")
                        # Update path to match reality if needed
                        path = f"bronze/liquicomun/{year}/{month}/{downloaded_name}"
                    
                    storage.save(path, content)
                    logger.info(f"Stored: {path}")
                else:
                    logger.debug(f"No content for Liquicomun {archive_id} on {current_date.date()}")
                    
            except Exception as e:
                logger.error(f"Failed ID {archive_id} for {current_date.date()}: {e}")

        current_date += timedelta(days=1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download Liquicomun Data (Bronze)")
    parser.add_argument("--start-date", required=True, help="YYYY-MM-DD")
    parser.add_argument("--end-date", required=True, help="YYYY-MM-DD")
    args = parser.parse_args()
    
    start = datetime.strptime(args.start_date, "%Y-%m-%d")
    end = datetime.strptime(args.end_date, "%Y-%m-%d")
    
    logging.basicConfig(level=logging.INFO)
    download_liquicomun(start, end)
