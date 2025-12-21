import os
import time
import logging
from datetime import datetime, timedelta
from typing import List, Optional

from src.config import settings
from src.esios.client import EsiosClient
from src.storage.handler import StorageHandler

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def clean_older_versions(new_file_path: str):
    """
    Remove other files in the same directory of new_file_path.
    Used for A1/A2 types where only the latest version should be kept in that month folder.
    """
    try:
        folder = os.path.dirname(new_file_path)
        filename = os.path.basename(new_file_path)
        
        if not os.path.exists(folder):
            return

        for f in os.listdir(folder):
            if f != filename:
                full_path = os.path.join(folder, f)
                if os.path.isfile(full_path):
                    logging.info(f"Removing older version: {f}")
                    os.remove(full_path)
    except Exception as e:
        logging.error(f"Error cleaning older versions in {folder}: {e}")

def process_archive_family(family_id: int, dataset_name: str, date_obj: datetime, handler: StorageHandler, client: EsiosClient):
    """
    Finds and downloads archives for a specific family ID and date.
    Uses EsiosClient to download content.
    """
    # 1. Download Content
    # Client.download_archive returns (filename, content_bytes) or (filename, None)
    file_name, zip_bytes = client.download_archive(family_id, date_obj)
    
    if not zip_bytes:
        logging.info(f"[SKIP] ID {family_id} on {date_obj.date()}: No content.")
        return

    year_str = date_obj.strftime("%Y")
    month_str = date_obj.strftime("%m")

    # 2. Save and Unzip
    saved_path, _, _ = handler.save_raw_zip_and_unzip(
        dataset_name, year_str, month_str, file_name, zip_bytes
    )

    # 3. Clean older versions if applicable (Liquicomun A1/A2)
    # Logic: If saved_path is local and dataset is liquicomun, check subfolder
    if handler.mode == "local" and dataset_name == "liquicomun" and saved_path:
        # Path structure: .../raw/liquicomun/zips/A1/YYYY/MM/file.zip
        # We need to detect if we are in an "Only Latest" subfolder.
        # Handler saves to: raw/{dataset}/zips/{subfolder}/{year}/{month}
        # Let's check if any of the configured prefixes are in the path.
        path_parts = saved_path.replace("\\", "/").split("/")
        
        should_clean = True
        # Excepción: A1 y A2 son diarios, mantenemos todos los archivos del mes (historial diario)
        # El resto (C2, etc) solo queremos 1 al mes (el más reciente/definitivo)
        for keep_daily in ["A1", "A2"]:
            # Si la ruta contiene A1 o A2, NO limpiamos (False)
            if f"/{keep_daily}/" in saved_path.replace("\\", "/"):
                should_clean = False
                break
        
        if should_clean:
            clean_older_versions(saved_path)

    logging.info(f"✅ Downloaded & Processed: {file_name}")


def run_daily_sync(start_date_str: str, end_date_str: Optional[str] = None):
    """
    Main entry point for daily synchronization of I3 and Liquicomun archives.
    Iterates through dates and downloads necessary files.
    """
    start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
    if end_date_str:
        end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()
    else:
        end_date = datetime.now().date()

    client = EsiosClient()
    handler = StorageHandler()

    logging.info(f"--- Starting Daily Sync: {start_date} to {end_date} ---")

    current_date = start_date
    while current_date <= end_date:
        logging.info(f"📅 Processing Date: {current_date}")
        current_dt = datetime.combine(current_date, datetime.min.time())

        # Process I90 (ID 34)
        if hasattr(settings, "ESIOS_I90_ID"):
             process_archive_family(settings.ESIOS_I90_ID, "i90", current_dt, handler, client)

        # Process I3 (ID 32)
        if hasattr(settings, "ESIOS_I3_ID"):
             process_archive_family(settings.ESIOS_I3_ID, "i3", current_dt, handler, client)
        
        # Process Liquicomun (2-11)
        if hasattr(settings, "ESIOS_LIQUICOMUN_IDS"):
            for fid in settings.ESIOS_LIQUICOMUN_IDS:
                # Determine if we should attempt download
                # Rules:
                # 1. If ID is in ESIOS_LIQUICOMUN_DAILY_IDS (A1, A2), download daily.
                # 2. Others: Only download if we don't have a file for this ID + Month yet.
                
                is_daily = fid in getattr(settings, "ESIOS_LIQUICOMUN_DAILY_IDS", [])
                
                should_download = False
                if is_daily:
                    should_download = True
                else:
                    # Check if exists for this month
                    # Note: We use current_dt to check the month we are processing
                    year_s = current_dt.strftime("%Y")
                    month_s = current_dt.strftime("%m")
                    if not handler.exists_monthly_file("liquicomun", fid, year_s, month_s):
                        should_download = True
                    # else: passing silently to avoid log spam, or can debug log
                
                if should_download:
                    process_archive_family(fid, "liquicomun", current_dt, handler, client)
        
        current_date += timedelta(days=1)
        # Sleep slightly to avoid rate limits if aggressive
        time.sleep(0.2)

    logging.info("--- Daily Sync Completed ---")

def backfill_archive(archive_id: int, dataset_name: str, start_date_str: str, end_date_str: Optional[str] = None):
    """
    Legacy/Specific backfill for a single ID.
    """
    start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
    if end_date_str:
        end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()
    else:
        end_date = datetime.now().date()

    client = EsiosClient()
    handler = StorageHandler()
    
    current_date = start_date
    while current_date <= end_date:
        current_dt = datetime.combine(current_date, datetime.min.time())
        process_archive_family(archive_id, dataset_name, current_dt, handler, client)
        current_date += timedelta(days=1)