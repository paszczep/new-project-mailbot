
_Application made for a Polish client._

Aplikacja wysyła wiadomości e-mail zawierającą informacje dotyczące nowego projektu na adresy:

- kierownika projektu,
- osoby odpowiedzialnej,
- odpowiedniego handlowca,
- działu - w zależności od grupy projektu.

# emails.toml

Konfiguracja działowych adresów email.

`always` - zawsze otrzymują wiadomość,

`group` - otrzymują wiadomość dla określonych grup projektu.

# .env

Aresy i uwierzytelnienia do bazy danych i SMTP.

```
postgres_user=
postgres_password=
postgres_host=
postgres_database=

email_user=
email_password=
email_port=
email_server=
```

# Makefile

`make go` - uruchom

`make logs` - logi

`make kill` - zatrzymaj i usuń kontener

