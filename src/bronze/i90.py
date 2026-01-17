import logging
import argparse
from datetime import datetime, timedelta
from src.common.client import EsiosClient
from src.common.filesystem import StorageManager
from src.config import settings

logger = logging.getLogger(__name__)

def download_i90(start_date: datetime, end_date: datetime):
    """
    Downloads I90 files for the specified date range.
    """
    client = EsiosClient()
    storage = StorageManager()
    
    current_date = start_date
    while current_date <= end_date:
        archive_id = settings.ESIOS_I90_ID
        
        logger.info(f"Checking/Downloading I90 for {current_date.date()}...")
        
        # Check if already exists (optional optimization, client handles download)
        # We'll use the client to get the filename and content
        
        try:
            filename, content = client.download_archive(archive_id, current_date)
            
            if content:
                # Path: bronze/i90/YYYY/MM/filename
                year = current_date.strftime("%Y")
                month = current_date.strftime("%m")
                path = f"bronze/i90/{year}/{month}/{filename}"
                
                storage.save(path, content)
                logger.info(f"Stored: {path}")
            else:
                logger.warning(f"No content for I90 on {current_date.date()}")
                
        except Exception as e:
            logger.error(f"Failed to download I90 for {current_date.date()}: {e}")

        current_date += timedelta(days=1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download I90 Data (Bronze)")
    parser.add_argument("--start-date", required=True, help="YYYY-MM-DD")
    parser.add_argument("--end-date", required=True, help="YYYY-MM-DD")
    args = parser.parse_args()
    
    start = datetime.strptime(args.start_date, "%Y-%m-%d")
    end = datetime.strptime(args.end_date, "%Y-%m-%d")
    
    logging.basicConfig(level=logging.INFO)
    download_i90(start, end)
