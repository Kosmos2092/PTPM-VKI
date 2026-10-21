import sqlite3

BY_SIDES = "side_a = ? AND side_b = ? AND side_c = ?"


class TriangleDatabase:
    """Результаты расчётов в SQLite. Запись определяется тремя введёнными длинами сторон."""

    def __init__(self, path: str = ":memory:"):
        self.connection = sqlite3.connect(path)
        self.connection.execute(
            "CREATE TABLE IF NOT EXISTS triangles ("
            "side_a TEXT, side_b TEXT, side_c TEXT, kind TEXT, error TEXT, "
            "PRIMARY KEY (side_a, side_b, side_c))"
        )

    def add(self, a: str, b: str, c: str, kind: str, error: str | None) -> None:
        with self.connection:  # сохраняет изменения в файл БД
            self.connection.execute("INSERT INTO triangles VALUES (?, ?, ?, ?, ?)", (a, b, c, kind, error))

    def get(self, a: str, b: str, c: str) -> tuple[str, str | None] | None:
        """Возвращает (вид, ошибка) или None, если записи нет."""
        return self.connection.execute(f"SELECT kind, error FROM triangles WHERE {BY_SIDES}", (a, b, c)).fetchone()

    def delete(self, a: str, b: str, c: str) -> None:
        with self.connection:
            self.connection.execute(f"DELETE FROM triangles WHERE {BY_SIDES}", (a, b, c))

    def close(self) -> None:
        self.connection.close()
