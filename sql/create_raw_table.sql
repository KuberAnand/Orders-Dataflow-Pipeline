CREATE OR REPLACE TABLE ecommerce_dw.raw_orders
(
order_id STRING,
order_date DATE,
customer_id STRING,
customer_name STRING,
email STRING,
product_name STRING,
category STRING,
quantity INT64,
unit_price FLOAT64,
revenue FLOAT64,
store_name STRING
);