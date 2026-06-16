from google.cloud import bigquery

client = bigquery.Client()

table_id = "de-course-488205.ecommerce_dw.raw_orders"

job_config = bigquery.LoadJobConfig(
    skip_leading_rows=1,
    source_format=bigquery.SourceFormat.CSV,
    autodetect=True,
    write_disposition="WRITE_TRUNCATE"
)

with open(
    "/opt/airflow/data/orders.csv",
    "rb"
) as source_file:

    load_job = client.load_table_from_file(
        source_file,
        table_id,
        job_config=job_config
    )

load_job.result()

print("Loaded")