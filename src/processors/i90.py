from src.processors.base import BaseProcessor
import pandas as pd

class I90Processor(BaseProcessor):
    def __init__(self):
        super().__init__("i90")
        
    def process_file(self, file_path: str):
        """
        Implementación específica para i90.
        """
        print(f"[{self.dataset_name.upper()}] Procesando: {file_path}")
        
        # AQUI VA LA LOGICA DE PARSEO (XML/CSV/ETC)
        # Ejemplo Dummy:
        # data = parse_i90_xml(file_path)
        # db.insert(data)
        
        return "Processed (Dummy)"
