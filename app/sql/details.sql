SELECT
    
    CONCAT(
        TRIM(proj.own_number), ' ',
        TRIM(order.investor), '/',
        TRIM(order.object_name), '/',
        TRIM(order.contractor_short)
    )                                               AS project_identifier,

    
    TRIM(contractor.contractor_name)                AS contractor_name,
    
    TRIM(regexp_replace(TRIM(order.scope),
                        E'[\\n\\r]+', ' ', 'g'))    AS project_group,

    
    salesperson.description                         AS salesperson_name,

    
    TRIM(responsible.first_name) || ' ' || TRIM(responsible.last_name)
                                                    AS responsible_name,

    responsible_extra.email                         AS responsible_email,
    
    TRIM(main.customer_order_number)                AS order_number,

    
    datasql(main.realization_date)                  AS completion_date,

    
    datasql_ifnotzero(order.expected_date)          AS expected_date,

    
    sales_extra.email                               AS salesperson_email,

    
    note.note                                       AS remark,

    
    features.field1                                 AS offer_number,

    
    TRIM(manager.first_name) || ' ' || TRIM(manager.last_name)
                                                    AS project_manager,

    manager_extra.email                             AS manager_email



FROM erp.client_orders                     main
JOIN erp.contractors                      b    ON b.id_contractor        = main.id_contractor
JOIN erp.project_links                    link ON (link.source_type,
                                                link.source_id1,
                                                link.source_id2)      = (3, main.year, main.number)
JOIN erp.projects                         proj ON (proj.number, proj.year)
                                                 = (link.project_number, link.project_year)

LEFT JOIN erp.client_order_commissions    comm ON (comm.lp,
                                                 comm.order_number,
                                                 comm.order_year)     = (1, main.number, main.year)
LEFT JOIN erp.salespersons                salesperson       ON salesperson.code = comm.salesperson_id
LEFT JOIN erp.users                       user              ON user.employee_id = salesperson.employee_id
LEFT JOIN erp.users_extra                 sales_extra       ON sales_extra.user_id = user.user_id
LEFT JOIN ar.project_managers             mgr_link          ON (mgr_link.number, mgr_link.year) = (proj.number, proj.year)


LEFT JOIN LATERAL (
    SELECT
        o.investor                        AS investor,
        o.object_name,
        o.scope,
        o.expected_date,
        c.short_name                      AS contractor_short
    FROM ar.customer_orders o
    LEFT JOIN erp.contractors c
           ON c.id_contractor = o.client_id
    WHERE o.year = main.year
      AND o.number = main.number
    LIMIT 1
) order ON TRUE

LEFT JOIN LATERAL (
    SELECT c.contractor_name
    FROM erp.client_orders co
    JOIN erp.contractors     c ON c.id_contractor = co.id_contractor
    WHERE co.year = main.year
      AND co.number = main.number
    LIMIT 1
) contractor ON TRUE

LEFT JOIN LATERAL (
    SELECT note
    FROM erp.client_order_notes
    WHERE order_year = main.year
      AND order_number = main.number
      AND lp = 1
    LIMIT 1
) note ON TRUE

LEFT JOIN LATERAL (
    SELECT field1
    FROM erp.client_order_features
    WHERE order_year       = main.year
      AND order_number     = main.number
      AND feature_type_id  = 2
      AND feature_value_id = 2
    LIMIT 1
) features ON TRUE


LEFT JOIN erp.employees responsible         ON responsible.code   = proj.responsible_id
LEFT JOIN abc.user_cards responsible_rcp    ON responsible_abc.employee_code = responsible.code
LEFT JOIN erp.users_extra responsible_extra ON responsible_extra.user_id = responsible_abc.user_id


LEFT JOIN erp.employees manager           ON manager.code = mgr_link.manager_id
LEFT JOIN abc.user_cards manager_rcp      ON manager_abc.employee_code = manager.code
LEFT JOIN erp.users_extra manager_extra   ON manager_extra.user_id = manager_abc.user_id


WHERE (main.number, main.year) = (:order_number, :order_year);
