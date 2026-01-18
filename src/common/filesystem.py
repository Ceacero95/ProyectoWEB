"""
filesystem.py

OBJECTIVE:
    Manages local file system interactions for the Bronze Layer.
    Acts as an abstraction layer for saving and checking the existence of raw files (ZIPs, JSONs)
    before they are processed by the Silver Layer.

DESIGN PATTERN:
    - This class is designed to be easily extensible for Cloud Storage (GCS/S3) by replacing
      internal method logic without changing the public API used by downloaders.

USAGE:
    storage = StorageManager()
    storage.save("bronze/omie/file.zip", content_bytes)
    if storage.exists("bronze/omie/file.zip"): ...

"""
import os
import shutil
import logging
from typing import List, Optional
from src.config import settings

logger = logging.getLogger(__name__)

class StorageManager:
    """
    Abstracts filesystem operations to allow easy switching between Local, S3, GCS, etc.
    Currently implements Local storage.
    """
    
    def __init__(self, base_path: str = None):
        self.base_path = base_path or settings.LOCAL_DATA_DIR
        # In the future, we can initialize boto3/gcs clients here based on env vars
        
    def _get_full_path(self, relative_path: str) -> str:
        return os.path.join(self.base_path, relative_path)

    def save(self, relative_path: str, content: bytes, overwrite: bool = True):
        full_path = self._get_full_path(relative_path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        
        mode = "wb" if overwrite else "xb"
        try:
            with open(full_path, mode) as f:
                f.write(content)
            logger.info(f"Saved file to {full_path}")
        except FileExistsError:
            logger.warning(f"File {full_path} already exists. Skipping.")

    def read(self, relative_path: str) -> Optional[bytes]:
        full_path = self._get_full_path(relative_path)
        if not os.path.exists(full_path):
            return None
        with open(full_path, "rb") as f:
            return f.read()

    def exists(self, relative_path: str) -> bool:
        full_path = self._get_full_path(relative_path)
        return os.path.exists(full_path)

    def list_files(self, relative_path: str, extension: str = None) -> List[str]:
        """
        Returns a list of RELATIVE paths of files in the directory.
        """
        full_path = self._get_full_path(relative_path)
        if not os.path.exists(full_path):
            return []
            
        files = []
        for root, _, filenames in os.walk(full_path):
            for filename in filenames:
                if extension and not filename.endswith(extension):
                    continue
                # Construct relative path from base_path specifically
                abs_file = os.path.join(root, filename)
                rel_file = os.path.relpath(abs_file, self.base_path)
                files.append(rel_file)
        return files
