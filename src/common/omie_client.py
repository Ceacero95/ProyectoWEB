import requests
import logging
from datetime import datetime
import os

logger = logging.getLogger(__name__)

class OmieClient:
    """
    Client for downloading public files from OMIE.
    Base URL: https://www.omie.es/es/file-download?parents=marginalpdbc&filename=...
    """
    
    BASE_URL = "https://www.omie.es/es/file-download"
    
    def download_file(self, filename: str) -> requests.Response:
        """
        Downloads a specific file from OMIE.
        """
        # The 'parents' parameter seems to match the file type/directory on OMIE.
        # For 'marginalpdbc', parents is 'marginalpdbc'.
        # We can detect 'parents' from the filename prefix if needed, or pass it.
        # For now, we assume 'marginalpdbc' based on user request.
        
        parents = "marginalpdbc"
        if "marginalpdbc" in filename:
            parents = "marginalpdbc"
        elif "marginalpibc" in filename:
            parents = "marginalpibc"
        elif "pdbc" in filename:
            parents = "pdbc"
        elif "pdbf" in filename:
            parents = "pdbf"
        elif "pdvd" in filename:
            parents = "pdvd"
        elif "trades" in filename:
            parents = "trades"
            
        params = {
            "parents": parents,
            "filename": filename
        }
        
        url = self.BASE_URL
        try:
            logger.info(f"Downloading {filename} from OMIE...")
            response = requests.get(url, params=params, timeout=30)
            
            if response.status_code == 404:
                logger.info(f"File {filename} not found (404).")
                return None
                
            response.raise_for_status()
            
            # Check if content is actually a file or an HTML error page
            if "text/html" in response.headers.get("Content-Type", ""):
                # OMIE might return 200 OK with HTML content for "File not found"
                logger.warning(f"Response for {filename} was HTML. Possible file not found.")
                return None
                
            return response
        except requests.exceptions.RequestException as e:
            logger.error(f"Error downloading {filename}: {e}")
            return None

    def get_marginalpdbc_filename(self, date: datetime) -> str:
        """
        Returns the expected filename for a given date.
        Logic:
        - Year < 2023: marginalpdbc_YYYY.zip (Annual Zip)
        - Year >= 2023: marginalpdbc_YYYYMMDD.1 (Daily file)
        """
        if date.year < 2023:
            return f"marginalpdbc_{date.year}.zip"
        else:
            date_str = date.strftime("%Y%m%d")
            return f"marginalpdbc_{date_str}.1"
