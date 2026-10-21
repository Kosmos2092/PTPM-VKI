import logging
from abc import ABC, abstractmethod

log = logging.getLogger(__name__)


class Notifier(ABC):
    """Интерфейс передачи результата сторонней системе."""

    @abstractmethod
    def send(self, message: str) -> None:
        """Передаёт строку-результат."""


class EmailNotifier(Notifier):
    """Имитация email-сервера: письмо не отправляется, а только записывается в лог."""

    def __init__(self, address: str):
        self.address = address

    def send(self, message: str) -> None:
        log.info(f"Письмо на {self.address}: {message}")
