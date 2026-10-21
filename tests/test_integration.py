import logging
import unittest
from unittest.mock import Mock

from src.controller import Controller
from src.database import TriangleDatabase
from src.notifier import Notifier
from src.triangle import TriangleCalculator, log as triangle_log
from src.user_input import UserInput

triangle_log.addHandler(logging.NullHandler())  # чтобы логи не засоряли вывод тестов


class TestControllerIntegration(unittest.TestCase):
    """Настоящие вычисления и БД (SQLite в памяти); ввод пользователя и отправка письма — заглушки."""

    def setUp(self):
        self.database = TriangleDatabase()
        self.addCleanup(self.database.close)
        self.calculator = Mock(wraps=TriangleCalculator())  # считает по-настоящему и запоминает вызовы
        self.user_input = Mock(spec=UserInput)
        self.notifier = Mock(spec=Notifier)
        self.controller = Controller(self.calculator, self.database, self.user_input, self.notifier)

    def run_with(self, *sides):
        self.user_input.get_sides.return_value = sides
        return self.controller.run()

    def test_new_sides_are_calculated_and_saved_to_db(self):
        self.assertEqual(self.run_with("3", "4", "5"), "разносторонний")
        self.assertEqual(self.database.get("3", "4", "5"), ("разносторонний", None))

    def test_known_sides_are_taken_from_db_without_calculation(self):
        self.database.add("3", "4", "5", "разносторонний", None)
        self.assertEqual(self.run_with("3", "4", "5"), "разносторонний")
        self.calculator.calculate.assert_not_called()

    def test_repeated_request_is_calculated_only_once(self):
        self.run_with("3", "3", "3")
        self.run_with("3", "3", "3")
        self.calculator.calculate.assert_called_once()

    def test_result_is_sent_to_notifier(self):
        self.run_with("5", "5", "8")
        self.notifier.send.assert_called_once_with("равнобедренный")

    def test_invalid_input_is_saved_with_error_message(self):
        self.assertEqual(self.run_with("abc", "4", "5"), "Ошибка: некорректные данные")
        self.assertEqual(self.database.get("abc", "4", "5"), ("", "некорректные данные"))

    def test_not_triangle_is_saved_with_error_message(self):
        self.assertEqual(self.run_with("1", "2", "3"), "Ошибка: стороны не образуют треугольник")
        self.assertEqual(self.database.get("1", "2", "3"), ("не треугольник", "стороны не образуют треугольник"))


if __name__ == "__main__":
    unittest.main()
