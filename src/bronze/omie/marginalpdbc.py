import logging
from datetime import datetime, timedelta
import os
from src.common.filesystem import StorageManager
from src.common.omie_client import OmieClient

logger = logging.getLogger(__name__)

def download_marginalpdbc(start_date: datetime, end_date: datetime):
    """
    Downloads OMIE marginalpdbc files for the specified date range.
    """
    storage = StorageManager()
    client = OmieClient()
    
    # We iterate by year to handle pre-2023 zips efficiently 
    # (avoid downloading the same zip 365 times if possible, though simple logic is fine for now)
    # Actually, iterate by day to respect start/end range, but cache year-zips if needed?
    # Simpler: Iterate by day. If year < 2023, check if we already have the year zip.
    
    processed_years_zips = set()
    
    current_date = start_date
    while current_date <= end_date:
        filename = client.get_marginalpdbc_filename(current_date)
        year = current_date.strftime("%Y")
        month = current_date.strftime("%m")
        
        # Define target path in Bronze
        # Format: bronze/omie/marginalpdbc/{year}/{month}/filename
        # For Zips (annual), maybe just bronze/omie/marginalpdbc/{year}/filename ?
        # User requested "separation in bronze". 
        # If it's a zip covering the whole year, putting it in "month" folder of the requested date might be confusing 
        # but if we are downloading it "for that date", it's tricky.
        # Best approach: 
        # - Daily files (.1) -> bronze/omie/marginalpdbc/{year}/{month}/...
        # - Annual Zips -> bronze/omie/marginalpdbc/{year}/...
        
        if filename.endswith(".zip"):
            if year in processed_years_zips:
                current_date += timedelta(days=1)
                continue
                
            target_path = f"bronze/omie/marginalpdbc/{year}/{filename}"
            processed_years_zips.add(year)
        else:
            target_path = f"bronze/omie/marginalpdbc/{year}/{month}/{filename}"
            
        if storage.exists(target_path):
            logger.info(f"File {target_path} already exists. Skipping download.")
        else:
            response = client.download_file(filename)
            if response:
                storage.save(target_path, response.content)
            else:
                logger.warning(f"Failed to download {filename}")
        
        current_date += timedelta(days=1)
