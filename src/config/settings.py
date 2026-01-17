import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# --- ESIOS API CONFIGURATION ---
ESIOS_TOKEN = os.getenv("ESIOS_TOKEN")
# Fallback hardcoded URL if env var is missing or specific override needed
ESIOS_BASE_ARCHIVE_URL = os.getenv("ESIOS_BASE_ARCHIVE_URL", "https://api.esios.ree.es/archives/")

# IDs de Archivos ESIOS
ESIOS_I3_ID = int(os.getenv("ESIOS_I3_ID", 32))      # I03
ESIOS_I90_ID = int(os.getenv("ESIOS_I90_ID", 34))    # I90
# IDs Liquicomun: 2 a 11. Se pueden configurar en ENV o usar default.
_liquicomun_ids = os.getenv("ESIOS_LIQUICOMUN_IDS", "2,3,4,5,6,7,8,9,10,11")
ESIOS_LIQUICOMUN_IDS = [int(x.strip()) for x in _liquicomun_ids.split(",") if x.strip().isdigit()]

# IDs que se descargan DIARIAMENTE (A1=2, A2=3). El resto: Mensual (día 1).
ESIOS_LIQUICOMUN_DAILY_IDS = [2, 3]

# --- DATABASE CONFIGURATION ---
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "postgres")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASS = os.getenv("DB_PASS", "password")

# Construcción de la URL de conexión (SQLAlchemy style)
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# --- PATHS ---
# Directorio raíz del proyecto
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
LOCAL_DATA_DIR = os.path.join(BASE_DIR, "local_data")

# Asegurar que existan directorios base
os.makedirs(LOCAL_DATA_DIR, exist_ok=True)