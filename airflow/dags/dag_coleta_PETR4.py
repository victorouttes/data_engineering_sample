import requests
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
import tempfile


def get_yahoo_finance_petrobras(day: str):
    start_date = datetime.strptime(f'{day} 00:00:00', '%Y-%m-%d %H:%M:%S') - timedelta(days=5)
    end_date = datetime.strptime(f'{day} 23:59:59', '%Y-%m-%d %H:%M:%S')
    period_start = int(start_date.timestamp())
    period_end = int(end_date.timestamp())
    stock = 'PETR4.SA'
    url = f"https://query1.finance.yahoo.com/v7/finance/download/{stock}?period1={period_start}&period2={period_end}&interval=1d&events=history&includeAdjustedClose=true"
    response = requests.get(
        url=url,
        headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                               "Chrome/58.0.3029.110 Safari/537.3"}
    )
    response.raise_for_status()

    with tempfile.NamedTemporaryFile() as temporary_file:
        temporary_file.write(response.content)
        temporary_file.flush()

        s3 = S3Hook('VERTICAL_S3')
        s3.load_file(
            filename=temporary_file.name,
            key=f'{stock}/collected_{day}.csv',
            bucket_name='vertical',
            replace=True
        )


default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=1),
}

dag = DAG(
    dag_id="dag_coleta_PETR4",
    description="Uma DAG para coletar dados do Yahoo Finance do dia da execucao usando a biblioteca requests",
    default_args=default_args,
    schedule_interval=timedelta(days=5),
    start_date=datetime(2023, 4, 1),
    catchup=True,
)

fetch_data_task = PythonOperator(
    task_id="get_yahoo_finance_petrobras",
    python_callable=get_yahoo_finance_petrobras,
    dag=dag,
    op_kwargs={'day': '{{ ds }}'}
)

fetch_data_task
