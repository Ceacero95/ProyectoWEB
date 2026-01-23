import sys
from datetime import datetime
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Añadir ruta del proyecto
sys.path.append("/opt/airflow")

from src.silver.omie.marginalpdbc import process_marginalpdbc

def run_db_ingest_only():
    # Definir rango de fechas para Enero 2026
    start_date = datetime(2026, 1, 1)
    end_date = datetime(2026, 1, 31)
    
    print(f"--- REPROCESANDO MARGINALPDBC (Silver -> Gold/DB) ---")
    print(f"Rango: {start_date.date()} a {end_date.date()}")
    
    try:
        # Ejecutamos process_marginalpdbc.
        # Esta función lee de Bronze (que ya debe estar descargado) y escribe en DB.
        process_marginalpdbc(start_date, end_date)
        print("Procesamiento completado con éxito.")
    except Exception as e:
        print(f"Error crítico: {e}")

if __name__ == "__main__":
    run_db_ingest_only()
