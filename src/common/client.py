import requests
import logging
from datetime import datetime
from src.config.settings import ESIOS_TOKEN

logger = logging.getLogger(__name__)

class EsiosClient:
    """
    Client to interact with ESIOS Public Archives.
    Standard implementation using Hostname.
    MOVED from src/ingestion/client.py to src/common/client.py
    """
    def __init__(self, token=None):
        self.base_url = "https://api.esios.ree.es/archives/"
        self.token = token or ESIOS_TOKEN
        
    def download_archive(self, archive_id: int, date: datetime) -> tuple[str, bytes] | tuple[str, None]:
        """
        Downloads a ZIP archive for a specific ID and Date.
        """
        start_date_str = date.strftime("%Y-%m-%dT00:00:00+00:00")
        end_date_str = date.strftime("%Y-%m-%dT23:59:59+00:00")
        
        # URL construction
        url = (
            f"{self.base_url}{archive_id}/download?"
            f"date_type=default&"
            f"download_type=zip&"
            f"end_date={end_date_str}&"
            f"locale=es&"
            f"start_date={start_date_str}"
        )
        
        headers = {
            "Content-Type": "application/json"
        }
        
        if self.token:
            headers["Authorization"] = f"Token token=\"{self.token}\""
            headers["x-api-key"] = self.token
        
        try:
            response = requests.get(url, headers=headers, timeout=60)
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            if response.status_code == 404:
                # Common for non-existent dates/data
                return f"esios_{archive_id}_404", None
            logger.error(f"HTTP Error downloading {archive_id} for {date}: {e}")
            raise e
        except Exception as e:
            logger.error(f"Error downloading {archive_id} for {date}: {e}")
            raise e

        # Construct filename
        date_only_str = date.strftime("%Y%m%d")
        file_name = f"esios_{archive_id}_{date_only_str}.zip"
        
        if len(response.content) < 100: 
            # Likely empty zip or error message
            logger.info(f"Archive {archive_id} for {date} seems empty ({len(response.content)} bytes).")
            return file_name, None
        
        return file_name, response.content
