import os
from google.cloud import bigquery

PROJECT_ID = "de-course-488205"
DATASET = "ecommerce_dw"
RAW_TABLE = "raw_orders"

client = bigquery.Client(project=PROJECT_ID)

table_id = f"{PROJECT_ID}.{DATASET}.{RAW_TABLE}"
orders_file = os.getenv("ORDERS_FILE", "/opt/airflow/data/orders.csv")

schema = [
    bigquery.SchemaField("order_id", "STRING"),
    bigquery.SchemaField("order_date", "DATE"),
    bigquery.SchemaField("customer_id", "STRING"),
    bigquery.SchemaField("customer_name", "STRING"),
    bigquery.SchemaField("email", "STRING"),
    bigquery.SchemaField("city", "STRING"),
    bigquery.SchemaField("state", "STRING"),
    bigquery.SchemaField("product_name", "STRING"),
    bigquery.SchemaField("category", "STRING"),
    bigquery.SchemaField("quantity", "INT64"),
    bigquery.SchemaField("unit_price", "FLOAT64"),
    bigquery.SchemaField("revenue", "FLOAT64"),
    bigquery.SchemaField("store_name", "STRING"),
    bigquery.SchemaField("shipping_method", "STRING"),
    bigquery.SchemaField("shipping_status", "STRING"),
    bigquery.SchemaField("source_file_name", "STRING"),
    bigquery.SchemaField("loaded_at", "TIMESTAMP"),
]


def ensure_raw_table():
    table = bigquery.Table(table_id, schema=schema)

    table.clustering_fields = ["store_name", "customer_id"]

    client.create_table(table, exists_ok=True)

    table = client.get_table(table_id)

    existing_fields = {field.name for field in table.schema}
    missing_fields = [field for field in schema if field.name not in existing_fields]

    if missing_fields:
        table.schema = list(table.schema) + missing_fields
        client.update_table(table, ["schema"])


ensure_raw_table()

job_config = bigquery.LoadJobConfig(
    skip_leading_rows=1,
    source_format=bigquery.SourceFormat.CSV,
    schema=schema,
    write_disposition="WRITE_APPEND",
    schema_update_options=[bigquery.SchemaUpdateOption.ALLOW_FIELD_ADDITION],
)

with open(orders_file, "rb") as source_file:

    load_job = client.load_table_from_file(
        source_file,
        table_id,
        job_config=job_config
    )

load_job.result()

print(f"Loaded daily CSV into {table_id}")
