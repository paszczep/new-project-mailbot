from psycopg2 import connect
from psycopg2.extensions import connection as Psycopg2Connection
from typing import Literal
from pathlib import Path
from app.src.environment import Environment



class Database:
    """Dostęp do bazy danych."""

    _keys: dict = Environment.variables("postgres")
    _conn: Psycopg2Connection

    def __enter__(self):
        self._conn = connect(**self._keys)
        return self

    def __exit__(self, exc, *_):
        self._conn.close()

    def object(
        self, object: Literal["projects", "details", "elements", "update"]
    ) -> "Database":
        """Zaczytaj kwerendę."""
        file = Path(f"app/sql/{object}.sql")
        self._query: str = file.read_text()
        return self

    def arguments(self, **kwargs: dict[str, str]) -> "Database":
        """Uzupełnij kwerendę o argumenty."""
        for placeholder, value in kwargs.items():
            self._query = self._query.replace(f":{placeholder}", str(value))
        return self

    def fetch(self) -> list[dict]:
        """Pobierz wartości z bazy danych wraz z kluczami."""
        with self._conn.cursor() as cursor:
            cursor.execute(self._query)
            values = list(cursor.fetchall())
            columns = [desc[0] for desc in cursor.description]
            return [dict(zip(columns, row)) for row in values]

    def execute(self):
        """Aktualizuj bazę danych."""
        with self._conn.cursor() as cursor:
            cursor.execute(self._query)
            self._conn.commit()
