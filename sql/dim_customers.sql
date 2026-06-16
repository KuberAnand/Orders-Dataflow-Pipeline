CREATE OR REPLACE TABLE ecommerce_dw.dim_customers AS

SELECT DISTINCT

customer_id,
customer_name,
email,
city,
state

FROM ecommerce_dw.clean_orders
