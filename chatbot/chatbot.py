import os
from dotenv import load_dotenv
import google.generativeai as genai
from google.cloud import bigquery

PROJECT_ID = "de-course-488205"
DATASET = "ecommerce_dw"
MAX_BYTES_BILLED = 100 * 1024 * 1024
BLOCKED_SQL = ("INSERT", "UPDATE", "DELETE", "MERGE", "DROP", "TRUNCATE", "ALTER", "CREATE")

load_dotenv()

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

model = genai.GenerativeModel(
    "gemini-2.5-flash"
)

bq = bigquery.Client(project=PROJECT_ID)


def clean_sql(sql):
    sql = sql.strip().replace("```sql", "").replace("```", "").strip()
    upper_sql = sql.upper()
    if not (upper_sql.startswith("SELECT") or upper_sql.startswith("WITH")):
        raise ValueError("Only SELECT queries are allowed.")
    if any(keyword in upper_sql for keyword in BLOCKED_SQL):
        raise ValueError("Generated SQL contains a blocked keyword.")
    return sql


def run_safe_query(sql):
    dry_run_config = bigquery.QueryJobConfig(
        dry_run=True,
        use_query_cache=False,
        maximum_bytes_billed=MAX_BYTES_BILLED,
    )
    dry_run_job = bq.query(sql, job_config=dry_run_config)
    print(f"Estimated bytes scanned: {dry_run_job.total_bytes_processed}")

    run_config = bigquery.QueryJobConfig(maximum_bytes_billed=MAX_BYTES_BILLED)
    return bq.query(sql, job_config=run_config).to_dataframe()

while True:

    question = input(
        "\nQuestion: "
    )

    prompt = f"""
You are a careful analytics engineer for an e-commerce BI team.

Use BigQuery Standard SQL only.
Project: {PROJECT_ID}
Dataset: {DATASET}

fact_orders:
- order_id
- customer_id
- product_id
- store_id
- order_date
- quantity
- unit_price
- revenue
- shipping_method
- shipping_status

dim_customers:
- customer_id
- customer_name
- email
- city
- state

dim_products:
- product_id
- product_name
- category

dim_stores:
- store_id
- store_name

Relationships:
fact_orders.customer_id = dim_customers.customer_id
fact_orders.product_id = dim_products.product_id
fact_orders.store_id = dim_stores.store_id

Generate only one read-only BigQuery SQL query.
Use fully qualified table names like `{PROJECT_ID}.{DATASET}.fact_orders`.
Prefer aggregated results for business questions.

Do not include:
- ```sql
- ```
- explanations
- comments

Question:
{question}
"""

    sql = clean_sql(model.generate_content(
        prompt
    ).text)

    print("\nSQL:")
    print(sql)

    df = run_safe_query(sql)

    answer_prompt = f"""
Question: {question}

Query result:
{df.head(20).to_markdown(index=False)}

Answer in plain English for a non-technical stakeholder. Be concise and mention when the result is based on the displayed rows.
"""
    answer = model.generate_content(answer_prompt).text

    print("\nAnswer:")
    print(answer)
    print("\nData:")
    print(df)
