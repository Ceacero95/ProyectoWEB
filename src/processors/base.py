from abc import ABC, abstractmethod
import os

class BaseProcessor(ABC):
    """
    Clase base para procesadores de archivos ESIOS.
    Cada nuevo tipo de archivo (i90, i3, etc.) debe heredar de esta clase.
    """
    
    def __init__(self, dataset_name):
        self.dataset_name = dataset_name
        
    @abstractmethod
    def process_file(self, file_path: str):
        """
        Lógica específica para parsear y guardar los datos de un archivo.
        """
        pass
    
    def process_directory(self, directory_path: str):
        """
        Procesa todos los archivos en un directorio.
        """
        results = []
        for root, _, files in os.walk(directory_path):
            for file in files:
                full_path = os.path.join(root, file)
                try:
                    res = self.process_file(full_path)
                    results.append((file, "OK", res))
                except Exception as e:
                    results.append((file, "ERROR", str(e)))
        return results
