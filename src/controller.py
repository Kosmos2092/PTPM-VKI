import logging

from src.database import TriangleDatabase
from src.notifier import Notifier
from src.triangle import TriangleCalculator
from src.user_input import UserInput

ERRORS = {"": "некорректные данные", "не треугольник": "стороны не образуют треугольник"}

log = logging.getLogger(__name__)


class Controller:
    """Сквозной сценарий: ввод -> результат из БД или расчёт с сохранением -> отправка результата."""

    def __init__(self, calculator: TriangleCalculator, database: TriangleDatabase,
                 user_input: UserInput, notifier: Notifier):
        self.calculator = calculator
        self.database = database
        self.user_input = user_input
        self.notifier = notifier

    def run(self) -> str:
        sides = self.user_input.get_sides()
        record = self.database.get(*sides)
        if record:
            kind, error = record
            log.info(f"Результат для {sides} взят из БД")
        else:
            kind = self.calculator.calculate(*sides)[0]
            error = ERRORS.get(kind)
            self.database.add(*sides, kind, error)
            log.info(f"Результат для {sides} вычислен и сохранён в БД")

        result = f"Ошибка: {error}" if error else kind
        self.notifier.send(result)
        return result
