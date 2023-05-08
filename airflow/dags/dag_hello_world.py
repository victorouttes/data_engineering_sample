from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator


def print_hello():
    print("Hello World!")


default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=1),
}

dag = DAG(
    dag_id="dag_hello_world",
    description="Uma DAG simples com uma única tarefa para imprimir 'Hello World!'",
    default_args=default_args,
    schedule_interval=timedelta(minutes=2),
    start_date=datetime(2023, 1, 1),
    catchup=False,
)

t1 = PythonOperator(
    task_id="print_hello",
    python_callable=print_hello,
    dag=dag,
)

t1
