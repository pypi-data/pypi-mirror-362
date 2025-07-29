SELECT
  i_item_id,
  i_item_desc,
  i_category,
  i_class,
  i_current_price,
  SUM(ss_ext_sales_price) AS itemrevenue,
  SUM(ss_ext_sales_price) * 100 / SUM(SUM(ss_ext_sales_price)) OVER (PARTITION BY i_class) AS revenueratio
FROM store_sales, item, date_dim
WHERE
  ss_item_sk = i_item_sk
  AND i_category IN ('Music', 'Sports', 'Children')
  AND ss_sold_date_sk = d_date_sk
  AND d_date BETWEEN CAST('1998-03-14' AS DATE) AND (
    DATE_ADD(CAST('1998-03-14' AS DATE), 30)
  )
GROUP BY
  i_item_id,
  i_item_desc,
  i_category,
  i_class,
  i_current_price
ORDER BY
  i_category,
  i_class,
  i_item_id,
  i_item_desc,
  revenueratio