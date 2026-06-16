# Gemini chatbot placeholder
import os
from dotenv import load_dotenv
import google.generativeai as genai
from google.cloud import bigquery

load_dotenv()

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

model = genai.GenerativeModel(
    "gemini-2.5-flash"
)

bq = bigquery.Client(project="de-course-488205")

while True:

    question = input(
        "\nQuestion: "
    )

    prompt = f"""
Dataset: ecommerce_dw

fact_orders:
- order_id
- customer_id
- product_id
- order_date
- quantity
- revenue

dim_customers:
- customer_id
- customer_name
- city
- state

dim_products:
- product_id
- product_name
- category

Relationships:
fact_orders.customer_id = dim_customers.customer_id
fact_orders.product_id = dim_products.product_id

Generate only BigQuery SQL. 
dataset_id.table_id

Do not include:
- ```sql
- ```
- explanations
- comments

Question:
{question}
"""

    sql = model.generate_content(
        prompt
    ).text

    print("\nSQL:")
    print(sql)

    df = bq.query(sql).to_dataframe()

    print(df)