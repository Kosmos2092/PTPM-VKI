from abc import ABC, abstractmethod


class UserInput(ABC):
    """Интерфейс получения данных от пользователя."""

    @abstractmethod
    def get_sides(self) -> tuple[str, str, str]:
        """Возвращает три длины сторон в виде строк."""


class ConsoleInput(UserInput):
    def get_sides(self) -> tuple[str, str, str]:
        return tuple(input(f"Сторона {name}: ").strip() for name in "ABC")  # strip: '3 ' и '3' — одна запись в БД
