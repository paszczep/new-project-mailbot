from logging import info
from app.src.objects import Order, Details, Element
from app.src.message import Message
from app.src.database import Database
from app.src.send import Email


def process_order(db: Database,  order: Order):
    """Jeśli nowy projekt obejmuje elementy, wyślij informację do aktorów."""
    if elements := Element.fetch(db, order):
        details = Details.fetch(db, order)
        info(f'Projekt z grupy: {details.project_group}.')
        message = Message(details=details, elements=elements)
        
        Email(
            recipients=(rs := message.recipients()),
            subject=message.subject(),
            content=message.content()
        ).send()

        order.update(db)
        
        info(f'Wysłano wiadomość do odbiorców: {', '.join(rs)}')


def job():
    with Database() as db:
        orders = Order.fetch(db)
        info(f'Nowe projekty: {len(orders)}.')
        for order in orders:
            process_order(db, order)
