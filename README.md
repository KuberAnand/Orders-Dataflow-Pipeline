# Orders-Dataflow-Pipeline

E-commerce orders pipeline on GCP and BigQuery.

## Architecture

Local assessment flow:

```text
Synthetic daily CSV
  -> Airflow DAG
  -> BigQuery raw_orders
  -> SQL cleaning and star schema
  -> automated quality gates
  -> Gemini + BigQuery chatbot prototype
```

Production GCP version:

```text
Email attachment
  -> Gmail API or Cloud Function
  -> GCS landing bucket
  -> Cloud Composer / Airflow
  -> BigQuery raw partitioned table
  -> BigQuery clean and dimensional tables
  -> quality checks + alerting
  -> BI dashboards and chatbot
```

## What This Solves

- Automates the daily CSV ingestion workflow with Airflow.
- Loads order data into BigQuery.
- Cleans duplicates, missing dates, negative revenue, and inconsistent product names.
- Builds a simple star schema for analytics.
- Runs quality checks automatically and fails the pipeline if final warehouse data is not trustworthy.
- Provides a chatbot prototype for non-technical users to ask plain-English questions.

## BigQuery Tables

Raw layer:

- `raw_orders`: append-only daily CSV load with source file and load timestamp metadata.

Clean layer:

- `clean_orders`: deduplicated and standardized order records.

Analytics layer:

- `fact_orders`: order-level facts with customer, product, and store keys.
- `dim_customers`: customer attributes.
- `dim_products`: standardized product names and categories.
- `dim_stores`: online store dimension.


## Data Quality Rules

The source data intentionally contains realistic issues:

- duplicate order IDs
- missing order dates
- negative revenue
- inconsistent product names such as `PATIO CHAIR` and `patio-chair`

The final quality gate checks:

- no duplicate orders in clean data
- no null order dates
- no negative revenue
- revenue matches `quantity * unit_price`
- every fact row has matching customer, product, and store dimension records
- final fact table is not empty

If any rule fails, the Airflow task raises an error and downstream dashboard/chatbot consumers should not use the data.

## Cost And Reliability Choices

- Daily batch loading is simpler and cheaper than streaming for emailed CSVs.
- BigQuery partitioning limits scanned data for time-based queries.
- Clustering improves common joins and filters.
- The chatbot uses dry-run query estimates and a maximum bytes billed limit.
- Airflow retries handle temporary failures.
- Raw data is append-only so failed transformations can be replayed.

## Run Locally

1. Configure Google Cloud authentication locally.
2. Set required environment variables in `.env`, including:

```text
FERNET_KEY=...
AIRFLOW__API_AUTH__JWT_SECRET=...
GEMINI_API_KEY=...
```

3. Start Airflow:

```bash
docker compose up
```

4. Create the BigQuery dataset/table if needed:

```bash
python test_bq.py
```

5. Trigger the Airflow DAG:

```text
ecommerce_pipeline
```

6. Try the chatbot:

```bash
python chatbot/chatbot.py
```

Example questions:

- How did we do last month?
- Which product sold the most?
- Which store has the highest revenue?

## Known Limitations

- The email ingestion step is represented locally by synthetic CSV generation.
- In production, the CSV receiver should use Gmail API or Cloud Function to save attachments to GCS.
- Secrets should be stored in Secret Manager, not local `.env` files.
- The chatbot is a prototype and should be deployed behind authentication with stricter semantic-layer controls.
