
CREATE OR REPLACE TABLE ecommerce_dw.fact_orders AS

SELECT

order_id,
order_date,
customer_id,
CAST(ABS(FARM_FINGERPRINT(LOWER(product_name))) AS STRING) AS product_id,
CAST(ABS(FARM_FINGERPRINT(LOWER(store_name))) AS STRING) AS store_id,
quantity,
unit_price,
revenue,
shipping_method,
shipping_status

FROM ecommerce_dw.clean_orders
