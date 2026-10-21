import logging
import sys
from pathlib import Path

from src.controller import Controller
from src.database import TriangleDatabase
from src.notifier import EmailNotifier
from src.triangle import TriangleCalculator
from src.user_input import ConsoleInput

SRC_DIR = Path(__file__).parent
LOG_DIR = SRC_DIR / "logs"
DB_PATH = SRC_DIR / "triangles.db"
EMAIL = "teacher@example.com"

log = logging.getLogger(__name__)


def setup_logging():
    LOG_DIR.mkdir(exist_ok=True)
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s | [%(levelname)-7s] | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler(LOG_DIR / "file_txt.log", encoding="utf-8"),
        ],
    )


def main():
    setup_logging()
    log.info("Приложение запущено")
    database = TriangleDatabase(DB_PATH)
    controller = Controller(TriangleCalculator(), database, ConsoleInput(), EmailNotifier(EMAIL))
    print(f"Результат: {controller.run()}")
    database.close()
    log.info("Приложение завершено")


if __name__ == "__main__":  # pragma: no cover — только при прямом запуске
    main()
