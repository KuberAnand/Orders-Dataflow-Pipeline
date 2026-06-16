-- cleaning sql
CREATE OR REPLACE TABLE ecommerce_dw.clean_orders
 AS

WITH standardized AS
(
SELECT *,
CASE
    WHEN LOWER(REPLACE(TRIM(product_name), '-', ' ')) = 'patio chair' THEN 'Patio Chair'
    ELSE INITCAP(REPLACE(TRIM(product_name), '-', ' '))
END AS normalized_product_name,
ROUND(quantity * unit_price, 2) AS calculated_revenue
FROM ecommerce_dw.raw_orders
),

dedup AS
(
SELECT *
FROM standardized
QUALIFY ROW_NUMBER() OVER
(
PARTITION BY order_id
ORDER BY loaded_at DESC, order_date DESC
) = 1
)

SELECT
order_id,
order_date,
customer_id,
customer_name,
email,
city,
state,
normalized_product_name AS product_name,
category,
quantity,
unit_price,
calculated_revenue AS revenue,
store_name,
shipping_method,
shipping_status,
source_file_name,
loaded_at

FROM dedup

WHERE order_date IS NOT NULL
AND revenue > 0
AND quantity > 0
AND unit_price > 0
