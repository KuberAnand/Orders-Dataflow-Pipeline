
CREATE OR REPLACE TABLE ecommerce_dw.dim_products AS

SELECT DISTINCT

CAST(ABS(FARM_FINGERPRINT(LOWER(product_name))) AS STRING) AS product_id,
product_name,
category

FROM ecommerce_dw.clean_orders
