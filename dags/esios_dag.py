
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
from datetime import datetime, timedelta
import sys
import os

# Add src to sys.path so we can import internal modules
sys.path.append("/opt/airflow")
from src.bronze.liquicomun import download_liquicomun
from src.silver.liquicomun_parquet import ingest_to_parquet
from src.silver.liquicomun import process_liquicomun

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'esios_liquicomun_pipeline',
    default_args=default_args,
    description='Pipeline for ESIOS Liquicomun Data (Bronze -> Silver -> Gold)',
    schedule=None, # Manual execution
    start_date=days_ago(1),
    catchup=False,
    tags=['esios', 'energy'],
) as dag:

    def _bronze_task(**context):
        # By default run for "yesterday" if not specified
        # execution_date in Airflow is the START of the interval, so data_interval_end is usually "today"
        target_date = context['data_interval_end'].date() - timedelta(days=1)
        # Or just use today? Usually we want yesterday's data or today's.
        # Let's target the logical date.
        # If run on 2026-01-18 at 08:00, we probably want data for 2026-01-18 or 17.
        # Let's download for the execution day.
        
        # Access config to override dates manually via "Trigger DAG w/ config"
        conf = context.get('dag_run').conf or {}
        start = conf.get('start_date')
        end = conf.get('end_date')

        if start and end:
            s_date = datetime.strptime(start, '%Y-%m-%d')
            e_date = datetime.strptime(end, '%Y-%m-%d')
        else:
            # Default: Run for "yesterday" relative to potential availability
            # Note: Airflow logical_date is usually "yesterday" for daily scheduled jobs.
            s_date = context['logical_date']
            e_date = context['logical_date']

        print(f"Downloading from {s_date} to {e_date}")
        download_liquicomun(s_date, e_date)
        # Return dates to pass to next task
        return {'start': s_date.strftime('%Y-%m-%d'), 'end': e_date.strftime('%Y-%m-%d')}

    def _silver_task(**context):
        # Pull dates from bronze task
        dates = context['ti'].xcom_pull(task_ids='download_bronze')
        s = datetime.strptime(dates['start'], '%Y-%m-%d')
        e = datetime.strptime(dates['end'], '%Y-%m-%d')
        print(f"Ingesting Silver for {s} - {e}")
        ingest_to_parquet(s, e)
        return dates

    def _gold_task(**context):
        dates = context['ti'].xcom_pull(task_ids='ingest_silver')
        s = datetime.strptime(dates['start'], '%Y-%m-%d')
        e = datetime.strptime(dates['end'], '%Y-%m-%d')
        print(f"Processing Gold for {s} - {e}")
        process_liquicomun(s, e)

    t1 = PythonOperator(
        task_id='download_bronze',
        python_callable=_bronze_task,
        provide_context=True
    )

    t2 = PythonOperator(
        task_id='ingest_silver',
        python_callable=_silver_task,
        provide_context=True
    )

    t3 = PythonOperator(
        task_id='process_gold',
        python_callable=_gold_task,
        provide_context=True
    )

    t1 >> t2 >> t3
