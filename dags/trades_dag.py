
"""
dags/trades_dag.py

OBJECTIVE:
    Orchestrates the daily/monthly ingestion of OMIE Trades data.
    Separated from the main OMIE pipeline to allow independent scheduling and backfilling.

SCHEDULE:
    - Daily at 10:00 UTC (0 10 * * *).
    
TASKS:
    1. download_trades: Fetches the ZIP for the current month.
    2. process_trades: Parses the daily file inside the ZIP and updates the DB.

MANUAL RUN:
    Can be triggered mainly for backfilling. 
    Accepts implicit 'logical_date' or explicit config params if extended.
"""
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import sys
import os

# Add project root to path
sys.path.append('/opt/airflow')

from src.bronze.omie.trades import download_trades
from src.silver.omie.trades import process_trades

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

def _download_task(download_func, **kwargs):
    logical_date = kwargs['logical_date'].replace(tzinfo=None) # Make naive
    # Start from 2025-01-01 to ensure holes are filled
    # 'download_trades' checks if ZIP exists, so it's efficient
    start_date = datetime(2025, 1, 1)
    end_date = logical_date # Up to execution date (or run end)
    
    # If logical_date is older than 2025 (backfill), just use that.
    if logical_date.year < 2025:
         start_date = logical_date.replace(day=1)
    
    # Ensure start <= end
    if start_date > end_date:
        start_date = end_date

    download_func(start_date, end_date)


def _process_task(process_func, parent_task_id, **kwargs):
    logical_date = kwargs['logical_date'].replace(tzinfo=None) # Make naive
    # Scan full year (or from 2025)
    # Processing logic will skip existing dates, so this efficiently fills gaps
    start_date = datetime(2025, 1, 1)
    end_date = logical_date
    
    if logical_date.year < 2025:
         start_date = logical_date

    if start_date > end_date:
        start_date = end_date

    process_func(start_date, end_date)


with DAG(
    'trades_pipeline',
    default_args=default_args,
    description='Pipeline for OMIE Trades data',
    schedule_interval='0 10 * * *', # Daily at 10:00 (Trades usually available later or early next day)
    start_date=datetime(2025, 1, 1),
    catchup=False,
    tags=['omie', 'trades'],
) as dag:

    t_down_trades = PythonOperator(
        task_id='download_trades',
        python_callable=_download_task,
        op_kwargs={'download_func': download_trades},
        provide_context=True
    )
    
    t_proc_trades = PythonOperator(
        task_id='process_trades',
        python_callable=_process_task,
        op_kwargs={'process_func': process_trades, 'parent_task_id': 'download_trades'},
        provide_context=True
    )
    
    t_down_trades >> t_proc_trades

    # --- Monitoring ---
    def _monitor_task(**kwargs):
        from src.common.monitoring import MonitoringManager
        monitor = MonitoringManager()
        monitor.update_control_table("trades", "omie")
        
    t_monitor = PythonOperator(
        task_id='monitor_trades',
        python_callable=_monitor_task
    )
    
    t_proc_trades >> t_monitor

