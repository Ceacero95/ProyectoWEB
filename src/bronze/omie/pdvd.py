import logging
from datetime import datetime
from src.common.filesystem import StorageManager
from src.common.omie_client import OmieClient

logger = logging.getLogger(__name__)

def download_pdvd(start_date: datetime, end_date: datetime):
    """
    Downloads OMIE pdvd files (Monthly ZIPs).
    Format: pdvd_YYYYMM.zip
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
            filename = f"pdvd_{year}{month}.zip"
            target_path = f"bronze/omie/pdvd/{year}/{filename}"
            
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
        
        if current_date.month == 12:
            current_date = current_date.replace(year=current_date.year+1, month=1, day=1)
        else:
            current_date = current_date.replace(month=current_date.month+1, day=1)
