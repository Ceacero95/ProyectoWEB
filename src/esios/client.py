# src/esios/client.py
import requests
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

class EsiosClient:
    def __init__(self, token=None):
        self.BASE_DOWNLOAD_URL = "https://api.esios.ree.es/archives/"
        self.token = token or os.getenv("ESIOS_TOKEN")
        
    def download_archive(self, archive_id, date: datetime) -> tuple[str, bytes] | tuple[str, None]:
        """
        Descarga el archivo ZIP de ESIOS y retorna el nombre de archivo 
        y el contenido binario (bytes). Retorna (nombre, None) si el contenido está vacío.
        """
        
        start_date_str = date.strftime("%Y-%m-%dT00:00:00+00:00")
        end_date_str = date.strftime("%Y-%m-%dT23:59:59+00:00")
        
        url = (
            f"{self.BASE_DOWNLOAD_URL}{archive_id}/download?"
            f"date_type=default&"
            f"download_type=zip&"
            f"end_date={end_date_str}&"
            f"locale=es&"
            f"start_date={start_date_str}"
        )
        
        headers = {}
        if self.token:
            headers = {
                "Authorization": f"Token token=\"{self.token}\"",
                "x-api-key": self.token,
                "Content-Type": "application/json"
            }
        
        response = requests.get(url, headers=headers)
        response.raise_for_status() 

        date_only_str = date.strftime("%Y%m%d")
        file_name = f"esios_{archive_id}_{date_only_str}.zip"
        
        if len(response.content) < 100: 
            return file_name, None  # Retorna None en lugar de los bytes
        
        return file_name, response.content