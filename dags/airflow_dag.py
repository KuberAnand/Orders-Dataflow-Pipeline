# Airflow DAG placeholder
from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

with DAG(
    dag_id="ecommerce_pipeline",
    start_date=datetime(2025,1,1),
    schedule="@daily",
    catchup=False
) as dag:

    generate = BashOperator(
        task_id="generate_orders",
        bash_command="uv run /opt/airflow/data_generation/generate_orders.py"
    )

    load = BashOperator(
        task_id="load_bigquery",
        bash_command="uv run /opt/airflow/pipeline/load_to_bigquery.py"
    )

    quality = BashOperator(
        task_id="quality_checks",
        bash_command="uv run /opt/airflow/pipeline/quality_checks.py"
    )

    etl = BashOperator(
        task_id="etl_flow",
        bash_command="uv run /opt/airflow/pipeline/etl.py"
    )

    generate >> load >> quality >> etl