
"""
data_ingestion/bronze/omie/trades.py

OBJECTIVE:
    Handles the downloading of 'Trades' data from OMIE.
    These files represent the actual energy trades matched in the market.
    Files are published Monthly as ZIP archives containing daily files.

FILE FORMAT:
    - Input: trades_YYYYMM.zip (e.g., trades_202501.zip)
    - Source: OMIE Public Website
    - Destination: bronze/omie/trades/YYYY/trades_YYYYMM.zip

LOGIC:
    - Iterates through requested dates by month.
    - Checks if the monthly ZIP already exists locally to avoid re-downloading.
    - Uses OmieClient with 'parents=trades'.
"""
import logging
from datetime import datetime
from src.common.filesystem import StorageManager
from src.common.omie_client import OmieClient

logger = logging.getLogger(__name__)

def download_trades(start_date: datetime, end_date: datetime):
    """
    Downloads OMIE trades files (Monthly ZIPs) covering the specified date range.
    
    Args:
        start_date (datetime): Start of the period (only Month/Year is used).
        end_date (datetime): End of the period.
    """
    storage = StorageManager()
    client = OmieClient()
    
    current_date = start_date.replace(day=1)
    processed_months = set()
    
    while current_date <= end_date:
        year = current_date.strftime("%Y")
        month = current_date.strftime("%m")
        key = f"{year}-{month}"
        
        if key not in processed_months:
            filename = f"trades_{year}{month}.zip"
            target_path = f"bronze/omie/trades/{year}/{filename}"
            
            if storage.exists(target_path):
                # Check if it is the current month
                now = datetime.now()
                is_current_month = (now.year == int(year) and now.month == int(month))
                
                if is_current_month:
                    logger.info(f"File {target_path} exists but is current month. Re-downloading to update.")
                    response = client.download_file(filename)
                    if response:
                        storage.save(target_path, response.content, overwrite=True)
                        processed_months.add(key)
                    else:
                        logger.warning(f"Failed to re-download {filename}")
                else:
                    logger.info(f"File {target_path} already exists (past month). Skipping.")
                    processed_months.add(key)
            else:
                response = client.download_file(filename)
                if response:
                    storage.save(target_path, response.content)
                    processed_months.add(key)
                else:
                    logger.warning(f"Failed to download {filename}")
        
        # Increment month
        if current_date.month == 12:
            current_date = current_date.replace(year=current_date.year+1, month=1, day=1)
        else:
            current_date = current_date.replace(month=current_date.month+1, day=1)
