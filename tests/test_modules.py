import logging
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from src import main
from src.database import TriangleDatabase
from src.notifier import EmailNotifier, Notifier
from src.user_input import ConsoleInput, UserInput


class TestDatabase(unittest.TestCase):
    def setUp(self):
        self.database = TriangleDatabase()
        self.addCleanup(self.database.close)

    def test_unknown_sides_have_no_record(self):
        self.assertIsNone(self.database.get("3", "4", "5"))

    def test_deleted_record_is_not_found(self):
        self.database.add("3", "4", "5", "разносторонний", None)
        self.database.delete("3", "4", "5")
        self.assertIsNone(self.database.get("3", "4", "5"))

    def test_record_persists_in_db_file(self):
        with TemporaryDirectory() as tmp:
            path = Path(tmp) / "test.db"
            first = TriangleDatabase(path)
            first.add("3", "4", "5", "разносторонний", None)
            first.close()
            reopened = TriangleDatabase(path)
            record = reopened.get("3", "4", "5")
            reopened.close()
        self.assertEqual(record, ("разносторонний", None))


class TestUserInput(unittest.TestCase):
    @patch("builtins.input", side_effect=["3", "4", "5"])  # заглушка ввода с клавиатуры
    def test_console_input_reads_three_sides(self, fake_input):
        self.assertEqual(ConsoleInput().get_sides(), ("3", "4", "5"))
        self.assertEqual(fake_input.call_count, 3)

    @patch("builtins.input", side_effect=[" 3 ", "4  ", "  5"])
    def test_console_input_strips_spaces_around_sides(self, _input):
        self.assertEqual(ConsoleInput().get_sides(), ("3", "4", "5"))

    def test_interfaces_cannot_be_instantiated(self):
        for interface in (UserInput, Notifier):
            with self.subTest(interface=interface.__name__), self.assertRaises(TypeError):
                interface()


class TestNotifier(unittest.TestCase):
    def test_email_notifier_only_imitates_sending(self):
        with self.assertLogs("src.notifier", "INFO") as logs:
            EmailNotifier("student@example.com").send("равносторонний")
        self.assertIn("student@example.com: равносторонний", logs.output[0])


class TestMain(unittest.TestCase):
    @patch("builtins.print")
    @patch("builtins.input", side_effect=["3", "4", "5"])
    @patch("src.main.DB_PATH", ":memory:")
    @patch("src.main.setup_logging")
    def test_main_runs_full_scenario(self, _setup_logging, _input, fake_print):
        main.main()
        fake_print.assert_called_once_with("Результат: разносторонний")

    def test_setup_logging_writes_to_console_and_file(self):
        with (TemporaryDirectory() as tmp,
              patch("src.main.LOG_DIR", Path(tmp) / "logs"),
              patch("logging.basicConfig") as basic_config):
            main.setup_logging()
            handlers = basic_config.call_args.kwargs["handlers"]
            for handler in handlers:
                handler.close()
        self.assertEqual([type(h) for h in handlers], [logging.StreamHandler, logging.FileHandler])


if __name__ == "__main__":
    unittest.main()
