import logging
from datetime import datetime, timedelta
import os
from src.common.filesystem import StorageManager
from src.common.omie_client import OmieClient

logger = logging.getLogger(__name__)

def download_marginalpibc(start_date: datetime, end_date: datetime):
    """
    Downloads OMIE marginalpibc files for the specified date range.
    Handles multiple markets/sessions per day.
    """
    storage = StorageManager()
    client = OmieClient()
    
    processed_years_zips = set()
    
    current_date = start_date
    while current_date <= end_date:
        year = current_date.strftime("%Y")
        month = current_date.strftime("%m")
        date_str = current_date.strftime("%Y%m%d")
        
        # Check annual zip logic
        zip_filename = f"marginalpibc_{year}.zip"
        zip_path = f"bronze/omie/marginalpibc/{year}/{zip_filename}"
        
        if year not in processed_years_zips:
             if storage.exists(zip_path):
                 processed_years_zips.add(year)
                 logger.info(f"Annual zip {zip_filename} found.")
             else:
                 # Try download
                 zip_resp = client.download_file(zip_filename)
                 if zip_resp:
                     storage.save(zip_path, zip_resp.content)
                     processed_years_zips.add(year)
                     logger.info(f"Downloaded annual zip {zip_filename}")
                 else:
                     # If zip download fails, we still mark the year as processed
                     # to avoid retrying for every day of the year.
                     # This assumes if it's not there once, it won't be there later.
                     # If a zip appears later, a re-run would pick it up.
                     processed_years_zips.add(year)
                     logger.debug(f"Annual zip {zip_filename} not found or failed to download. Proceeding with daily files for this year.")
        
        if storage.exists(zip_path):
             current_date += timedelta(days=1)
             continue

        # Format found on OMIE Access List: marginalpibc_YYYYMMDDMM.1 (e.g. marginalpibc_2025051601.1)
        # MM is likely session number (01, 02, 03...)
        # User restriction: Only sessions 1, 2, 3 exist.
        for i in range(1, 4):
            # Try 2-digit suffix + .1
            filename = f"marginalpibc_{date_str}{i:02d}.1"
            
            # Bronze path
            target_path = f"bronze/omie/marginalpibc/{year}/{month}/{filename}"
            
            if storage.exists(target_path):
                logger.info(f"File {target_path} already exists. Skipping.")
                continue
                
            response = client.download_file(filename)
            if response:
                storage.save(target_path, response.content)
            else:
                # Intraday sessions are finite and sequential.
                # If 1 fails, maybe error. If higher fails, likely end of sessions.
                # We stop iterating to save time and avoid 404s for 7, 8 etc if 6 was last.
                logger.debug(f"Failed to download {filename}. Stopping search for this day.")
                break
        
        current_date += timedelta(days=1)
