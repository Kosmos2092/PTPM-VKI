import logging
import sys
from pathlib import Path

from triangle import get_triangle

LOG_DIR = Path(__file__).parent / "logs"


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
    logging.info("Приложение запущено")
    a, b, c = (input(f"Сторона {name}: ") for name in "ABC")
    kind, points = get_triangle(a, b, c)
    print(f"Вид: {kind or 'некорректные данные'}, вершины: {points}")
    logging.info("Приложение завершено")


if __name__ == "__main__":
    main()
