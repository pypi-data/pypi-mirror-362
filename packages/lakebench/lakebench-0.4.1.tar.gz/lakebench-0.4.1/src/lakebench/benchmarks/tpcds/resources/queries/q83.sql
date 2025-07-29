WITH sr_items AS (
  SELECT
    i_item_id AS item_id,
    SUM(sr_return_quantity) AS sr_item_qty
  FROM store_returns, item, date_dim
  WHERE
    sr_item_sk = i_item_sk
    AND d_date IN (
      SELECT
        d_date
      FROM date_dim
      WHERE
        d_week_seq IN (
          SELECT
            d_week_seq
          FROM date_dim
          WHERE
            d_date IN ('1999-02-22', '1999-08-19', '1999-11-19')
        )
    )
    AND sr_returned_date_sk = d_date_sk
  GROUP BY
    i_item_id
), cr_items AS (
  SELECT
    i_item_id AS item_id,
    SUM(cr_return_quantity) AS cr_item_qty
  FROM catalog_returns, item, date_dim
  WHERE
    cr_item_sk = i_item_sk
    AND d_date IN (
      SELECT
        d_date
      FROM date_dim
      WHERE
        d_week_seq IN (
          SELECT
            d_week_seq
          FROM date_dim
          WHERE
            d_date IN ('1999-02-22', '1999-08-19', '1999-11-19')
        )
    )
    AND cr_returned_date_sk = d_date_sk
  GROUP BY
    i_item_id
), wr_items AS (
  SELECT
    i_item_id AS item_id,
    SUM(wr_return_quantity) AS wr_item_qty
  FROM web_returns, item, date_dim
  WHERE
    wr_item_sk = i_item_sk
    AND d_date IN (
      SELECT
        d_date
      FROM date_dim
      WHERE
        d_week_seq IN (
          SELECT
            d_week_seq
          FROM date_dim
          WHERE
            d_date IN ('1999-02-22', '1999-08-19', '1999-11-19')
        )
    )
    AND wr_returned_date_sk = d_date_sk
  GROUP BY
    i_item_id
)
SELECT
  sr_items.item_id,
  sr_item_qty,
  sr_item_qty / (
    sr_item_qty + cr_item_qty + wr_item_qty
  ) / 3.0 * 100 AS sr_dev,
  cr_item_qty,
  cr_item_qty / (
    sr_item_qty + cr_item_qty + wr_item_qty
  ) / 3.0 * 100 AS cr_dev,
  wr_item_qty,
  wr_item_qty / (
    sr_item_qty + cr_item_qty + wr_item_qty
  ) / 3.0 * 100 AS wr_dev,
  (
    sr_item_qty + cr_item_qty + wr_item_qty
  ) / 3.0 AS average
FROM sr_items, cr_items, wr_items
WHERE
  sr_items.item_id = cr_items.item_id AND sr_items.item_id = wr_items.item_id
ORDER BY
  sr_items.item_id,
  sr_item_qty
LIMIT 100