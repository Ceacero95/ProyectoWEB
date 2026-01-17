import logging
from datetime import datetime
from src.common.filesystem import StorageManager
from src.common.omie_client import OmieClient

logger = logging.getLogger(__name__)

def download_pdbf(start_date: datetime, end_date: datetime):
    """
    Downloads OMIE pdbf files (Monthly ZIPs).
    Format: pdbf_YYYYMM.zip
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
            filename = f"pdbf_{year}{month}.zip"
            target_path = f"bronze/omie/pdbf/{year}/{filename}"
            
            if storage.exists(target_path):
                logger.info(f"File {target_path} already exists. Skipping.")
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
