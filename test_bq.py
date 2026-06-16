from google.cloud import bigquery
from pathlib import Path

client = bigquery.Client(project="de-course-488205")

dataset_id = "de-course-488205.ecommerce_dw"

dataset = bigquery.Dataset(dataset_id)

dataset.location = "US"

client.create_dataset(dataset, exists_ok=True)

create_raw_table_sql = Path("sql/create_raw_table.sql").read_text()
client.query(create_raw_table_sql).result()

print("Dataset and raw table are ready")
