# src/storage/handler.py
import os
import io
import zipfile
from src.config.settings import GCS_BUCKET, LOCAL_DATA_ROOT 

# Define la base del directorio local
RAW_DATA_ROOT = os.path.join(LOCAL_DATA_ROOT, "raw")

class StorageHandler:
    def __init__(self, bucket_name=GCS_BUCKET):
        # Default to localhost if not set, ensuring local mode works by default
        if os.getenv("DB_HOST", "localhost") == "localhost":
            print("INFO: Modo Almacenamiento Local.", flush=True)
            # No creamos directorios específicos aquí, se crearán bajo demanda
            self.mode = "local"
        else:
            print("INFO: Modo Almacenamiento GCP.")
            from google.cloud import storage # Lazy import
            self.client = storage.Client()
            self.bucket = self.client.bucket(bucket_name)
            self.mode = "gcp"

    def _get_path(self, dataset_name: str, year_str: str, month_str: str, filename: str, file_type: str) -> str:
        """
        Construye la ruta del objeto (GCS) o la ruta de archivo (Local).
        file_type: 'zips' o 'decompressed'
        """
        if self.mode == "gcp":
            # Ruta de objeto GCS: raw/{dataset_name}/{file_type}/YYYY/MM/filename
            return f"raw/{dataset_name}/{file_type}/{year_str}/{month_str}/{filename}"
        else:
            # Ruta de archivo local: local_data/raw/{dataset_name}/{file_type}/YYYY/MM/filename
            target_dir = os.path.join(RAW_DATA_ROOT, dataset_name, file_type, year_str, month_str)
            os.makedirs(target_dir, exist_ok=True)
            return os.path.join(target_dir, filename)

    def save_raw_zip_and_unzip(self, dataset_name: str, year_str: str, month_str: str, file_name: str, zip_bytes: bytes) -> tuple:
        """
        Guarda el ZIP en la ruta raw/{dataset_name}/zips/[SUBTIPO]/YYYY/MM.
        Si es local, también lo descomprime en decompressed/YYYY/MM/[SUBTIPO].
        
        Para 'liquicomun', detecta automáticamente el subtipo (A1, A2, C2...) leyendo el contenido del ZIP.
        """
        
        subfolder = ""
        
        # Detección inteligente de subtipo para liquicomun
        if dataset_name == "liquicomun":
            try:
                with zipfile.ZipFile(io.BytesIO(zip_bytes)) as z:
                    # Buscamos un patrón común. Usualmente los archivos empiezan por el tipo (ej: A5_...)
                    # Tomamos el primer archivo que contenga un guion bajo
                    for name in z.namelist():
                        if "_" in name:
                            possible_prefix = name.split("_")[0]
                            # Validación simple: que sea corto (ej A1, C2)
                            if len(possible_prefix) <= 3 and possible_prefix.isalnum():
                                subfolder = possible_prefix
                                break
            except Exception as e:
                print(f"Warning: No se pudo detectar subtipo para liquicomun: {e}")

        # Construimos las rutas
        # Si detectamos subtipo, lo añadimos a la estructura de carpetas
        # Estructura: raw/liquicomun/zips/A5/2025/01/archivo.zip
        
        if subfolder:
            final_file_type_zip = f"zips/{subfolder}"
            final_file_type_dec = f"decompressed/{subfolder}"
        else:
            final_file_type_zip = "zips"
            final_file_type_dec = "decompressed"

        # 1. Guardar el archivo ZIP
        # Nota: _get_path usa 'file_type' como parte del path. Lo ajustamos aquí.
        # hack: pasamos todo el string "zips/A5" como file_type
        
        # Sin embargo, _get_path hace: raw/{dataset}/{file_type}/{year}/{month}
        # Si pasamos 'zips/A5', queda: raw/liquicomun/zips/A5/2025/01... PERFECTO.
        
        zip_object_path = self._get_path(dataset_name, year_str, month_str, file_name, final_file_type_zip)

        if self.mode == "gcp":
            output = io.BytesIO(zip_bytes)
            blob = self.bucket.blob(zip_object_path)
            blob.upload_from_file(output, content_type='application/zip')
            return zip_object_path, None, f"GCP: Pendiente ({subfolder if subfolder else 'General'})"

        else: # Modo Local
            zip_path = zip_object_path
            with open(zip_path, 'wb') as f:
                f.write(zip_bytes)

            # Descomprimir
            decompressed_path = self._get_path(dataset_name, year_str, month_str, "", final_file_type_dec)
            unzipped_files = []
            try:
                with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                    zip_ref.extractall(decompressed_path)
                    unzipped_files = zip_ref.namelist()
                return zip_path, decompressed_path, unzipped_files
            except Exception as e:
                print(f"Error al descomprimir {zip_path}: {e}")
                return zip_path, None, None

    def upload_excel(self, dataframe, filename):
         if self.mode == "gcp":
             output = io.BytesIO()
             dataframe.to_excel(output, index=False)
             output.seek(0)
             blob = self.bucket.blob(f"output/{filename}")
             blob.upload_from_file(output, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
             print(f"Subido a GCS: output/{filename}")
         else:
             path = os.path.join("local_data/output_files", filename)
             os.makedirs(os.path.dirname(path), exist_ok=True)
             dataframe.to_excel(path, index=False)
             print(f"Guardado local: {path}")

    def exists_monthly_file(self, dataset_name: str, file_id: int, year_str: str, month_str: str) -> bool:
        """
        Verifica si existe ya un archivo para ese ID y Mes (independientemente del día exacto).
        Busca recursivamente dentro de raw/{dataset_name}/zips porque puede estar en subcarpetas (A1, C2, etc).
        """
        search_pattern = f"esios_{file_id}_{year_str}{month_str}" # Ej: esios_8_202512
        
        if self.mode == "local":
            base_dir = os.path.join(RAW_DATA_ROOT, dataset_name, "zips")
            if not os.path.exists(base_dir):
                return False
            
            # Buscar en todas las subcarpetas de zips/
            for root, dirs, files in os.walk(base_dir):
                for file in files:
                    # Comprobamos si el nombre contiene el patrón (ID + AÑOMES) y es .zip
                    if search_pattern in file and file.endswith(".zip"):
                        return True
            return False
        else:
            # Modo GCP
            prefix = f"raw/{dataset_name}/zips"
            try:
                blobs = self.client.list_blobs(self.bucket, prefix=prefix)
                for blob in blobs:
                    if search_pattern in blob.name and blob.name.endswith(".zip"):
                        return True
            except Exception as e:
                print(f"Error checking GCP existence: {e}")
            return False