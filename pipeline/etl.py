# pipeline/build_star_schema.py

from google.cloud import bigquery

PROJECT_ID = "de-course-488205"

client = bigquery.Client(project=PROJECT_ID)

sql_files = [
    "/opt/airflow/sql/clean_orders.sql",
    "/opt/airflow/sql/dim_customers.sql",
    "/opt/airflow/sql/dim_products.sql",
    "/opt/airflow/sql/fact_orders.sql"
]

for file in sql_files:
    print(f"Running {file}")

    with open(file) as f:
        query = f.read()
    print("FILE:", file)
    print("QUERY LENGTH:", len(query))
    print("QUERY PREVIEW:", query[:200])
    client.query(query).result()
    
print("All SQL executed successfully")