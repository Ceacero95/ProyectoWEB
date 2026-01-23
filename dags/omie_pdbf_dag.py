from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
from datetime import datetime
import sys

# Add src to pythonpath
sys.path.append("/opt/airflow")

from src.bronze.omie.pdbf import download_pdbf
from src.silver.omie.pdbf import process_pdbf

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

    if s_date.year >= 2025:
         real_start = datetime(2025, 1, 1)
         s_date = real_start
    
    download_pdbf(s_date, e_date)
    return {'start': s_date.strftime('%Y-%m-%d'), 'end': e_date.strftime('%Y-%m-%d')}

def _process_task(**context):
    dates = context['ti'].xcom_pull(task_ids='download_pdbf')
    s = datetime.strptime(dates['start'], '%Y-%m-%d')
    e = datetime.strptime(dates['end'], '%Y-%m-%d')
    process_pdbf(s, e)

def _monitor_task(**kwargs):
    from src.common.monitoring import MonitoringManager
    MonitoringManager().update_control_table("pdbf", "omie")

with DAG(
    'omie_pdbf_pipeline',
    default_args=default_args,
    description='Pipeline for OMIE PDBF (Curva Oferta) Data',
    schedule=None,
    start_date=days_ago(1),
    catchup=False,
    tags=['omie', 'pdbf'],
) as dag:

    t1 = PythonOperator(task_id='download_pdbf', python_callable=_download_task, provide_context=True)
    t2 = PythonOperator(task_id='process_pdbf', python_callable=_process_task, provide_context=True)
    t3 = PythonOperator(task_id='monitor_pdbf', python_callable=_monitor_task)

    t1 >> t2 >> t3
