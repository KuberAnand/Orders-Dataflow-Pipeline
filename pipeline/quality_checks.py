from google.cloud import bigquery

PROJECT_ID = "de-course-488205"
DATASET = "ecommerce_dw"

client = bigquery.Client(project=PROJECT_ID)

raw_profile_queries = {
    "raw_duplicate_order_ids": f"""
        SELECT COUNT(*) - COUNT(DISTINCT order_id)
        FROM `{PROJECT_ID}.{DATASET}.raw_orders`
    """,
    "raw_null_dates": f"""
        SELECT COUNT(*)
        FROM `{PROJECT_ID}.{DATASET}.raw_orders`
        WHERE order_date IS NULL
    """,
    "raw_negative_revenue": f"""
        SELECT COUNT(*)
        FROM `{PROJECT_ID}.{DATASET}.raw_orders`
        WHERE revenue < 0
    """,
}

quality_rules = {
    "clean_duplicate_order_ids": f"""
        SELECT COUNT(*) - COUNT(DISTINCT order_id)
        FROM `{PROJECT_ID}.{DATASET}.clean_orders`
    """,
    "clean_null_dates": f"""
        SELECT COUNT(*)
        FROM `{PROJECT_ID}.{DATASET}.clean_orders`
        WHERE order_date IS NULL
    """,
    "clean_negative_revenue": f"""
        SELECT COUNT(*)
        FROM `{PROJECT_ID}.{DATASET}.clean_orders`
        WHERE revenue < 0
    """,
    "fact_revenue_mismatch": f"""
        SELECT COUNT(*)
        FROM `{PROJECT_ID}.{DATASET}.fact_orders`
        WHERE ROUND(quantity * unit_price, 2) != revenue
    """,
    "fact_missing_customer_dimension": f"""
        SELECT COUNT(*)
        FROM `{PROJECT_ID}.{DATASET}.fact_orders` f
        LEFT JOIN `{PROJECT_ID}.{DATASET}.dim_customers` c
            ON f.customer_id = c.customer_id
        WHERE c.customer_id IS NULL
    """,
    "fact_missing_product_dimension": f"""
        SELECT COUNT(*)
        FROM `{PROJECT_ID}.{DATASET}.fact_orders` f
        LEFT JOIN `{PROJECT_ID}.{DATASET}.dim_products` p
            ON f.product_id = p.product_id
        WHERE p.product_id IS NULL
    """,
    "fact_missing_store_dimension": f"""
        SELECT COUNT(*)
        FROM `{PROJECT_ID}.{DATASET}.fact_orders` f
        LEFT JOIN `{PROJECT_ID}.{DATASET}.dim_stores` s
            ON f.store_id = s.store_id
        WHERE s.store_id IS NULL
    """,
    "fact_empty": f"""
        SELECT IF(COUNT(*) = 0, 1, 0)
        FROM `{PROJECT_ID}.{DATASET}.fact_orders`
    """,
}


def run_count(name, query):
    result = list(client.query(query).result())[0][0]
    print(f"{name}: {result}")
    return int(result)


print("Raw data profile. These issues are expected in the generated source file:")
for name, query in raw_profile_queries.items():
    run_count(name, query)

print("Final warehouse quality gates:")
failures = {}
for name, query in quality_rules.items():
    result = run_count(name, query)
    if result != 0:
        failures[name] = result

if failures:
    failure_text = ", ".join(f"{name}={count}" for name, count in failures.items())
    raise RuntimeError(f"Data quality checks failed: {failure_text}")

print("All final warehouse quality checks passed")
