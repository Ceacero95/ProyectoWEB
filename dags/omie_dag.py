
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
from datetime import datetime, timedelta
import sys

# Add src to pythonpath
sys.path.append("/opt/airflow")

from src.bronze.omie.pdbc import download_pdbc
from src.bronze.omie.pdbf import download_pdbf
from src.bronze.omie.pdvd import download_pdvd
# Assuming these exist based on file presence
from src.bronze.omie.marginalpdbc import download_marginalpdbc
from src.bronze.omie.marginalpibc import download_marginalpibc

from src.silver.omie.pdbc import process_pdbc
from src.silver.omie.pdbf import process_pdbf
from src.silver.omie.pdvd import process_pdvd
from src.silver.omie.marginalpdbc import process_marginalpdbc
from src.silver.omie.marginalpibc import process_marginalpibc

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'omie_pipeline',
    default_args=default_args,
    description='Pipeline for OMIE Data (Bronze -> Silver -> Gold)',
    schedule_interval='30 8 * * *', # Daily at 08:30
    start_date=days_ago(1),
    catchup=False,
    tags=['omie', 'energy'],
) as dag:

    # --- Generic Task Wrappers ---
    def _download_task(download_func, **context):
        # Default to "yesterday" or provided config dates
        conf = context.get('dag_run').conf or {}
        start = conf.get('start_date')
        end = conf.get('end_date')

        if start and end:
            s_date = datetime.strptime(start, '%Y-%m-%d')
            e_date = datetime.strptime(end, '%Y-%m-%d')
        else:
            s_date = context['logical_date']
            e_date = context['logical_date']

        print(f"Downloading {download_func.__name__} from {s_date} to {e_date}")
        download_func(s_date, e_date)
        return {'start': s_date.strftime('%Y-%m-%d'), 'end': e_date.strftime('%Y-%m-%d')}

    def _process_task(process_func, parent_task_id, **context):
        dates = context['ti'].xcom_pull(task_ids=parent_task_id)
        s = datetime.strptime(dates['start'], '%Y-%m-%d')
        e = datetime.strptime(dates['end'], '%Y-%m-%d')
        print(f"Processing {process_func.__name__} for {s} - {e}")
        process_func(s, e)

    # --- PDBC ---
    t_down_pdbc = PythonOperator(
        task_id='download_pdbc',
        python_callable=_download_task,
        op_kwargs={'download_func': download_pdbc},
        provide_context=True
    )
    t_proc_pdbc = PythonOperator(
        task_id='process_pdbc',
        python_callable=_process_task,
        op_kwargs={'process_func': process_pdbc, 'parent_task_id': 'download_pdbc'},
        provide_context=True
    )
    t_down_pdbc >> t_proc_pdbc

    # --- PDBF ---
    t_down_pdbf = PythonOperator(
        task_id='download_pdbf',
        python_callable=_download_task,
        op_kwargs={'download_func': download_pdbf},
        provide_context=True
    )
    t_proc_pdbf = PythonOperator(
        task_id='process_pdbf',
        python_callable=_process_task,
        op_kwargs={'process_func': process_pdbf, 'parent_task_id': 'download_pdbf'},
        provide_context=True
    )
    t_down_pdbf >> t_proc_pdbf

    # --- PDVD ---
    t_down_pdvd = PythonOperator(
        task_id='download_pdvd',
        python_callable=_download_task,
        op_kwargs={'download_func': download_pdvd},
        provide_context=True
    )
    t_proc_pdvd = PythonOperator(
        task_id='process_pdvd',
        python_callable=_process_task,
        op_kwargs={'process_func': process_pdvd, 'parent_task_id': 'download_pdvd'},
        provide_context=True
    )
    t_down_pdvd >> t_proc_pdvd

    # --- Marginal PDBC ---
    t_down_mar_pdbc = PythonOperator(
        task_id='download_marginal_pdbc',
        python_callable=_download_task,
        op_kwargs={'download_func': download_marginalpdbc},
        provide_context=True
    )
    t_proc_mar_pdbc = PythonOperator(
        task_id='process_marginal_pdbc',
        python_callable=_process_task,
        op_kwargs={'process_func': process_marginalpdbc, 'parent_task_id': 'download_marginal_pdbc'},
        provide_context=True
    )
    t_down_mar_pdbc >> t_proc_mar_pdbc

# ... (Imports preserved implicitly by multi_replace if structured well, but simple replace here)
from src.bronze.omie.trades import download_trades
from src.silver.omie.trades import process_trades

# ... (Existing DAG definition)

    # --- Marginal PIBC ---
    t_down_mar_pibc = PythonOperator(
        task_id='download_marginal_pibc',
        python_callable=_download_task,
        op_kwargs={'download_func': download_marginalpibc},
        provide_context=True
    )
    t_proc_mar_pibc = PythonOperator(
        task_id='process_marginal_pibc',
        python_callable=_process_task,
        op_kwargs={'process_func': process_marginalpibc, 'parent_task_id': 'download_marginal_pibc'},
        provide_context=True
    )
    t_down_mar_pibc >> t_proc_mar_pibc

    # --- Trades ---
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

