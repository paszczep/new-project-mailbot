SELECT
    x.item_id                   AS item_id,
    TRIM(y.index_name)          AS item_name,
    x.ordered_quantity          AS quantity,
    TRIM(y.unit)                AS unit,
    datesql(
        x.realization_date)     AS completion,
    datesql_ifnotzero(
        x.secondary_realization_date) AS deadline
FROM
    erp.client_order_items x
    INNER JOIN erp.abc_indexes y ON y.id_index = items.item_id
WHERE
    order_number = :order_number
    AND order_year = :order_year;
