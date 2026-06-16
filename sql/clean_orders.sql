-- cleaning sql
CREATE OR REPLACE TABLE ecommerce_dw.clean_orders AS

WITH dedup AS
(
SELECT *
FROM
(
SELECT *,
ROW_NUMBER() OVER
(
PARTITION BY order_id
ORDER BY order_date
) rn
FROM ecommerce_dw.raw_orders
)
WHERE rn=1
)

SELECT *

FROM dedup

WHERE order_date IS NOT NULL
AND revenue > 0