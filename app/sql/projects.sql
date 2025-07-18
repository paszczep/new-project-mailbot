SELECT
    nr   AS "number",
    rok  AS "year"
FROM
    abc.mail_new_project
WHERE
    "sent" = FALSE;