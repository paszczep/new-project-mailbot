from smtplib import SMTP
from ssl import create_default_context
from dataclasses import dataclass
from typing import ClassVar
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from app.src.environment import Environment


@dataclass(frozen=True)
class Sender:
    """Wartości kluczowe dla skrzynki email wysyłającej informacje."""
    user: str
    password: str
    port: int
    server: str

    @classmethod
    def values(cls) -> "Sender":
        return cls(**Environment.variables("email"))


@dataclass
class Email:
    """Wysyłana wiadomość email."""
    sender: ClassVar[Sender] = Sender.values()
    recipients: list[str]
    subject: str
    content: str

    def _msg(self) -> MIMEMultipart:
        message = MIMEMultipart("alternative")
        message["Subject"] = self.subject
        message["From"] = self.sender.user
        message["To"] = ", ".join(self.recipients)
        message.attach(MIMEText(self.content, "html"))
        return message

    def send(self):
        with SMTP(self.sender.server, self.sender.port) as server:
            server.starttls(context=create_default_context())
            server.login(self.sender.user, self.sender.password)
            server.sendmail(self.sender.user, self.recipients, self._msg().as_string())
