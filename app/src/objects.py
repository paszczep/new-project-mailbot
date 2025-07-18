from dataclasses import dataclass, fields
from datetime import date
from app.src.database import Database


@dataclass
class Order:
    """Rok i numery zamówienia projektów, dla których nie rozesłano jeszcze informacji."""

    year: str
    number: str

    @classmethod
    def fetch(cls, db: Database) -> list["Order"]:
        """Pobieranie wartości z bazy danych."""
        return [cls(**el) for el in db.object("projects").fetch()]

    def update(self, db: Database):
        """Aktualizacja bazy danych o rozesłaniu wiadomości."""
        db.object("update").arguments(
            order_year=self.year, order_number=self.number
        ).execute()


@dataclass
class Element:
    """Produkt, element zamówienia."""

    item_id: str
    # item: str
    item_name: str
    quantity: float | str
    unit: str
    completion: date
    deadline: date | None

    @staticmethod
    def labels() -> list[str]:
        return [
            "Kod",
            "Nazwa indeksu",
            "Ilość",
            "Jm.",
            "Termin realizacji",
            "Oczekiwana data",
        ]

    def quantity_str(self) -> str:
        """Poprawna reprezentacja liczby całkowitej jako tekst."""
        try:
            if self.unit == ".szt" or self.quantity == int(self.quantity):
                return str(int(self.quantity))
            return str(self.quantity)
        except (ValueError, TypeError):
            return str(self.quantity)

    def __post_init__(self):
        self.completion = self.completion.isoformat()
        self.deadline = self.deadline.isoformat() if self.deadline else "-"
        self.quantity = self.quantity_str()

    @property
    def values(self) -> list[str]:
        """Wartości atrybutów w kolejności ich definicji.
        Konieczne do konstruowania tabeli z nagłówkami kolumn i wartościami 
        w odpowiadających pozycjach."""
        return [getattr(self, f.name) for f in fields(self)]

    @classmethod
    def fetch(cls, db: Database, order: Order) -> list["Element"]:
        """Pobieranie wartości z bazy danych."""
        return [
            cls(**el)
            for el in db.object("elements")
            .arguments(order_year=order.year, order_number=order.number)
            .fetch()
        ]


@dataclass
class Details:
    """Detale projektu/zamówienia klienta."""

    project_identifier: str
    contractor_name: str
    project_group: str
    salesperson_name: str | None
    responsible_name: str
    responsible_email: str
    order_number: str | None
    completion_date: date
    expected_date: date | None
    salesperson_email: str | None
    remark: str | None
    offer_number: str | None
    project_manager: str | None
    manager_email: str | None

    @property
    def emails(self) -> list[str]:
        """Adresy email osób związanych z projektem, na które wysyłana jest informacja."""
        return [
            v
            for f in fields(self)
            if f.name.endswith("email") and (v := getattr(self, f.name)) is not None
        ]

    @classmethod
    def fetch(cls, db: Database, order: Order) -> "Details":
        """Pobieranie wartości z bazy danych."""
        return cls(
            **db.object("details")
            .arguments(order_year=order.year, order_number=order.number)
            .fetch()
            .pop()
        )
