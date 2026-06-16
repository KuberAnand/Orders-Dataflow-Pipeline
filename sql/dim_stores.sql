CREATE OR REPLACE TABLE ecommerce_dw.dim_stores AS

SELECT DISTINCT

CAST(ABS(FARM_FINGERPRINT(LOWER(store_name))) AS STRING) AS store_id,
store_name

FROM ecommerce_dw.clean_orders
