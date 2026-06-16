
CREATE OR REPLACE TABLE ecommerce_dw.dim_products AS

SELECT DISTINCT

product_name,
category

FROM ecommerce_dw.clean_orders