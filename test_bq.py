from google.cloud import bigquery

client = bigquery.Client(project="de-course-488205")

dataset_id = "de-course-488205.ecommerce_dw"

dataset = bigquery.Dataset(dataset_id)

dataset.location = "US"

client.create_dataset(dataset, exists_ok=True)

print("Dataset Created")