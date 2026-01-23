from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
from datetime import datetime
import sys

# Add src to pythonpath
sys.path.append("/opt/airflow")

from src.bronze.omie.marginalpdbc import download_marginalpdbc
from src.silver.omie.marginalpdbc import process_marginalpdbc

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
        # Default behavior: Run from start of current month to today
        # This ensures manual trigger fills gaps for the month.
        now = datetime.now()
        s_date = datetime(now.year, now.month, 1)
        e_date = now.replace(hour=0, minute=0, second=0, microsecond=0)
    
    download_marginalpdbc(s_date, e_date)
    return {'start': s_date.strftime('%Y-%m-%d'), 'end': e_date.strftime('%Y-%m-%d')}

def _process_task(**context):
    dates = context['ti'].xcom_pull(task_ids='download_marginalpdbc')
    s = datetime.strptime(dates['start'], '%Y-%m-%d')
    e = datetime.strptime(dates['end'], '%Y-%m-%d')
    process_marginalpdbc(s, e)

def _monitor_task(**kwargs):
    from src.common.monitoring import MonitoringManager
    MonitoringManager().update_control_table("marginalpdbc", "omie")

with DAG(
    'omie_marginalpdbc_pipeline',
    default_args=default_args,
    description='Pipeline for OMIE Marginal PDBC (Precios Diario) Data',
    schedule=None,
    start_date=days_ago(1),
    catchup=False,
    tags=['omie', 'marginalpdbc'],
) as dag:

    t1 = PythonOperator(task_id='download_marginalpdbc', python_callable=_download_task, provide_context=True)
    t2 = PythonOperator(task_id='process_marginalpdbc', python_callable=_process_task, provide_context=True)
    t3 = PythonOperator(task_id='monitor_marginalpdbc', python_callable=_monitor_task)

    t1 >> t2 >> t3
