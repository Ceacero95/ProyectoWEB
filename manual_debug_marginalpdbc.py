import sys
from datetime import datetime
import logging

# Configurar logging para ver la salida en terminal
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Añadir ruta del proyecto
sys.path.append("/opt/airflow")

from src.bronze.omie.marginalpdbc import download_marginalpdbc
from src.silver.omie.marginalpdbc import process_marginalpdbc

def run_manual_test():
    # Definir rango de fechas para prueba (Enero 2026 completo)
    start_date = datetime(2026, 1, 1)
    end_date = datetime(2026, 1, 31)
    
    print(f"--- INICIANDO TEST MANUAL: {start_date.date()} a {end_date.date()} ---")
    
    print("1. Descargando datos (Bronze)...")
    try:
        download_marginalpdbc(start_date, end_date)
        print("Descarga completada sin errores críticos.")
    except Exception as e:
        print(f"Error en descarga: {e}")
        
    print("\n2. Procesando datos (Silver -> Gold/DB)...")
    try:
        process_marginalpdbc(start_date, end_date)
        print("Procesamiento completado.")
    except Exception as e:
        print(f"Error en procesado: {e}")

if __name__ == "__main__":
    run_manual_test()
