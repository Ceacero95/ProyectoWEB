import logging
from datetime import datetime, timedelta
from src.common.filesystem import StorageManager
from src.common.omie_client import OmieClient

logger = logging.getLogger(__name__)

def download_pdbc(start_date: datetime, end_date: datetime):
    """
    Downloads OMIE pdbc files (Monthly ZIPs).
    Format: pdbc_YYYYMM.zip
    """
    storage = StorageManager()
    client = OmieClient()
    
    current_date = start_date.replace(day=1) # Start at first of month
    
    processed_months = set()
    
    while current_date <= end_date:
        year = current_date.strftime("%Y")
        month = current_date.strftime("%m")
        key = f"{year}-{month}"
        
        if key in processed_months:
             # Move to next month logic handled at bottom?
             # If we increment by day, we hit this often.
             # Better to increment by month or check set.
             pass
        else:
            filename = f"pdbc_{year}{month}.zip"
            target_path = f"bronze/omie/pdbc/{year}/{filename}"
            
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
        
        # Increment to next month (simplistic: add 32 days then reset to day 1)
        # Or just increment by 1 day and let the set handle it? 
        # Ideally efficient loop:
        # if key in processed_months: next_month = ...
        # But end_date might be mid-month.
        # Simple: current_date += timedelta(days=1)
        # Check if month changed?
        
        # Optimization: Jump to next month.
        if current_date.month == 12:
            next_month = current_date.replace(year=current_date.year+1, month=1, day=1)
        else:
            next_month = current_date.replace(month=current_date.month+1, day=1)
            
        if next_month > end_date:
             # If next month is beyond end, we still might need to process the current month if end_date covers it.
             # But we just processed current_date (start of month).
             # So we represent the whole month.
             break
        current_date = next_month
