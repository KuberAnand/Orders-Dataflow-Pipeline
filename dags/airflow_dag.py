from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

default_args = {
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    dag_id="ecommerce_pipeline",
    description="Daily e-commerce CSV ingestion, BigQuery modeling, and quality gates",
    default_args=default_args,
    start_date=datetime(2025, 1, 1),
    schedule="@daily",
    catchup=False,
    tags=["ecommerce", "bigquery", "data-quality"]
) as dag:

    generate = BashOperator(
        task_id="generate_orders",
        bash_command="python /opt/airflow/data_generation/generate_orders.py"
    )

    load = BashOperator(
        task_id="load_bigquery",
        bash_command="python /opt/airflow/pipeline/load_to_bigquery.py"
    )

    etl = BashOperator(
        task_id="etl_flow",
        bash_command="python /opt/airflow/pipeline/etl.py"
    )

    quality = BashOperator(
        task_id="quality_checks",
        bash_command="python /opt/airflow/pipeline/quality_checks.py"
    )

    generate >> load >> etl >> quality
