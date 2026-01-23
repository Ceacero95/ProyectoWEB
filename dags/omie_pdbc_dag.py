from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
from datetime import datetime
import sys

# Add src to pythonpath
sys.path.append("/opt/airflow")

from src.bronze.omie.pdbc import download_pdbc
from src.silver.omie.pdbc import process_pdbc

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'retries': 1,
}

def _download_task(**context):
    conf = context.get('dag_run').conf or {}
    start = conf.get('start_date')
    end = conf.get('end_date')

    if start and end:
        s_date = datetime.strptime(start, '%Y-%m-%d')
        e_date = datetime.strptime(end, '%Y-%m-%d')
    else:
        s_date = context['logical_date'].replace(tzinfo=None)
        e_date = context['logical_date'].replace(tzinfo=None)

    # Force 2025 start regarding gap logic (optional, keep consistent with previous)
    if s_date.year >= 2025:
         real_start = datetime(2025, 1, 1)
         s_date = real_start
    
    download_pdbc(s_date, e_date)
    return {'start': s_date.strftime('%Y-%m-%d'), 'end': e_date.strftime('%Y-%m-%d')}

def _process_task(**context):
    dates = context['ti'].xcom_pull(task_ids='download_pdbc')
    s = datetime.strptime(dates['start'], '%Y-%m-%d')
    e = datetime.strptime(dates['end'], '%Y-%m-%d')
    process_pdbc(s, e)

def _monitor_task(**kwargs):
    from src.common.monitoring import MonitoringManager
    MonitoringManager().update_control_table("pdbc", "omie")

with DAG(
    'omie_pdbc_pipeline',
    default_args=default_args,
    description='Pipeline for OMIE PDBC (Curva Demanda) Data',
    schedule=None,
    start_date=days_ago(1),
    catchup=False,
    tags=['omie', 'pdbc'],
) as dag:

    t1 = PythonOperator(task_id='download_pdbc', python_callable=_download_task, provide_context=True)
    t2 = PythonOperator(task_id='process_pdbc', python_callable=_process_task, provide_context=True)
    t3 = PythonOperator(task_id='monitor_pdbc', python_callable=_monitor_task)

    t1 >> t2 >> t3
