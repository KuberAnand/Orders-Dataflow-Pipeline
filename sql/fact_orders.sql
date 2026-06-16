
CREATE OR REPLACE TABLE ecommerce_dw.fact_orders AS

SELECT

order_id,
order_date,
customer_id,
store_name,
quantity,
unit_price,
revenue

FROM ecommerce_dw.clean_orders