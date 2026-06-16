CREATE TABLE IF NOT EXISTS ecommerce_dw.raw_orders
(
order_id STRING,
order_date DATE,
customer_id STRING,
customer_name STRING,
email STRING,
city STRING,
state STRING,
product_name STRING,
category STRING,
quantity INT64,
unit_price FLOAT64,
revenue FLOAT64,
store_name STRING,
shipping_method STRING,
shipping_status STRING,
source_file_name STRING,
loaded_at TIMESTAMP
)
CLUSTER BY store_name, customer_id
