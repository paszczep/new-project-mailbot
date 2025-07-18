UPDATE
    abc.mail_new_project
SET
    sent = TRUE
WHERE
    number = :order_number
    AND year = :order_year
    ;