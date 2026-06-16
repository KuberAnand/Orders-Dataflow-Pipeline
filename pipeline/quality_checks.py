# Quality checks placeholder
from google.cloud import bigquery

client = bigquery.Client()

queries = {

"duplicates":"""
SELECT
COUNT(*)-COUNT(DISTINCT order_id)
FROM ecommerce_dw.raw_orders
""",

"null_dates":"""
SELECT COUNT(*)
FROM ecommerce_dw.raw_orders
WHERE order_date IS NULL
""",

"negative_revenue":"""
SELECT COUNT(*)
FROM ecommerce_dw.raw_orders
WHERE revenue < 0
"""
}

for name,q in queries.items():

    result = list(
        client.query(q).result()
    )[0][0]

    print(name,result)