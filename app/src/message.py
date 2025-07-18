from dataclasses import dataclass
from typing import ClassVar
from tomllib import load as load_toml
from pathlib import Path
from app.src.objects import Details, Element


@dataclass(frozen=True)
class _Config:
    """Skonfigurowane adresy email, na które wysyłana jest informacja."""

    always: list[str]
    group: dict[str, list[str]]

    @classmethod
    def load(cls) -> "_Config":
        _file = Path("emails.toml")
        with _file.open("rb") as _f:
            return cls(**load_toml(_f))


@dataclass
class Message:
    """Tytuł, treść i odbiorcy wiadomości z informacją o projekcie."""

    _style: ClassVar[str] = "style='border: 1px solid black; padding: 6px;'"
    _config: ClassVar[_Config] = _Config.load()

    details: Details
    elements: list[Element]

    def _header(self) -> str:
        """Nagłówek tabeli zawierający etykiety kolumn."""
        return "\n".join(
            [f"<th {self._style}><b>{el}</b></th>" for el in Element.labels()]
        )

    def _cell(self, value: str) -> str:
        """Komórka na wartość w tabeli."""
        return f"<td {self._style}>{value}</td>"

    def _row(self, element: Element):
        """Wiersz tabeli."""
        return "\n".join([f"{self._cell(val)}" for val in element.values])

    def _rows(self):
        """Wiersze w tabeli."""
        return "\n".join([f"<tr>{self._row(el)}</tr>" for el in self.elements])

    def _table(self) -> str:
        """Tabela zawierająca informacje o elementach projektu."""
        return f"""
            <table><thead><tr>
            {self._header()}
            </tr></thead><tbody>
            {self._rows()}
            </tbody></table>"""

    def _info(self):
        """Wypunktowane kluczowe informacje o projekcie."""
        o = self.details
        LABELS = {
            "Projekt": o.project_identifier,
            "Zamawiający": o.contractor_name,
            "Grupa": o.project_group,
            "Zamówienie": o.order_number,
            "Oferta": o.offer_number,
            "Handlowiec": o.salesperson_name,
            "Odpowiedzialny": o.responsible_name,
            "Kierownik": o.project_manager,
            "Uwagi": o.remark,
        }

        return "\n".join(
            [
                f"<li>{key}:{'&nbsp;'*3}<b>{value}</b></li>"
                for key, value in LABELS.items()
                if value is not None
            ]
        )

    def content(self) -> str:
        """Całkowita treść wiadomości."""
        return f"""
            <h3>Nowe zamówienie</h3>
            <p>
            <ul>
                {self._info()}
            </ul>
            </p>
            <p>
                {self._table()}
            </p>
            <p>
                Wiadomość wygenerowana automatycznie. Nie należy na nią odpowiadać.
            </p>
        """

    def subject(self) -> str:
        """Tytuł wiadomości email."""
        return f"Nowy projekt/zamówienie {self.details.project_identifier}"

    def recipients(self) -> set[str]:
        """Odbiorcy wiadomości email."""
        recipients: list[str] = []
        recipients += self._config.always
        recipients += self._config.group.get(self.details.project_group, [])
        recipients += self.details.emails
        return set(el.lower() for el in recipients)
