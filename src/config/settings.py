import os
from dotenv import load_dotenv
from datetime import datetime, timedelta

# Cargar variables del archivo .env
load_dotenv()

# --- CONFIGURACIÓN DE BASE DE DATOS ---
DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": os.getenv("DB_PORT", "5432"),
    "database": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASS"),
}

# --- CONFIGURACIÓN DE ALMACENAMIENTO Y ESIOS ---
GCS_BUCKET = os.getenv("GCS_BUCKET_NAME")
ESIOS_TOKEN = os.getenv("ESIOS_TOKEN")

# Definiciones de Rutas de Staging (capas de Data Lake)
RAW_PATH = "raw/"
PROCESSED_PATH = "processed/"
OUTPUT_PATH = "output/"

# Directorio local para simular GCS en desarrollo
LOCAL_DATA_ROOT = os.getenv("LOCAL_DATA_ROOT", "local_data")

# --- CONFIGURACIÓN ESIOS DINÁMICA ---

# URL Base para la descarga de archivos (la misma para I90, I3, Liquicomun, etc.)
ESIOS_BASE_ARCHIVE_URL = os.getenv("ESIOS_BASE_ARCHIVE_URL")

# Fecha de inicio para el proceso de carga histórica (backfill)
# Debe estar en formato "YYYY-MM-DD".
# I90_BACKFILL_START_DATE_STR = os.getenv("I90_BACKFILL_START_DATE", "2025-01-01")
I90_BACKFILL_START_DATE_STR = "2025-01-01" # Forzado por regla de negocio (Solo 2025)

# El retardo de liquidación (90 días es el estándar para liquidación definitiva)
I90_DAYS_DELAY = 90

# Conversión y comprobación de fechas
try:
    if I90_BACKFILL_START_DATE_STR:
        I90_BACKFILL_START_DATE = datetime.strptime(I90_BACKFILL_START_DATE_STR, "%Y-%m-%d").date()
    else:
        # Por defecto, 1 de Enero 2025
        I90_BACKFILL_START_DATE = datetime(2025, 1, 1).date()
except ValueError:
    raise ValueError("ERROR: La variable I90_BACKFILL_START_DATE debe tener formato YYYY-MM-DD.")


# --- COMPROBACIONES DE INTEGRIDAD ---

if not ESIOS_TOKEN:
    print("WARNING: ESIOS_TOKEN no está definido. La descarga de ESIOS fallará.")

# Asegurarse de que la URL base tiene la parte estática correcta
if not ESIOS_BASE_ARCHIVE_URL:
    print("WARNING: ESIOS_BASE_ARCHIVE_URL no está definida. La descarga fallará.")

# --- IDS DE ARCHIVOS ESIOS ---
# ID para el archivo I3 (Indisponibilidades)
ESIOS_I3_ID = int(os.getenv("ESIOS_I3_ID", 32))

# ID para I90 (PDBF)
ESIOS_I90_ID = int(os.getenv("ESIOS_I90_ID", 34))

# IDs para archivos de Liquicomun (2 a 11)
# Se pueden pasar como lista separada por comas en .env
_liquicomun_ids_env = os.getenv("ESIOS_LIQUICOMUN_IDS", "2,3,4,5,6,7,8,9,10,11")
ESIOS_LIQUICOMUN_IDS = [int(x.strip()) for x in _liquicomun_ids_env.split(",") if x.strip().isdigit()]

# Tipos de liquidación que requieren mantener solo la versión más reciente
LIQUICOMUN_ONLY_LATEST = ["A1", "A2"]

# IDs que se deben descargar diariamente (A1=2, A2=3). 
# El resto se descargan una vez al mes (día 1).
ESIOS_LIQUICOMUN_DAILY_IDS = [2, 3]