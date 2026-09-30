import logging
import math

FIELD_SIZE = 100
KINDS = {1: "равносторонний", 2: "равнобедренный", 3: "разносторонний"}  # по числу различных длин сторон

log = logging.getLogger(__name__)


def get_triangle(a: str, b: str, c: str) -> tuple[str, list[tuple[int, int]]]:
    """Возвращает вид треугольника и координаты его вершин в поле FIELD_SIZE x FIELD_SIZE."""
    params = f"a={a!r}, b={b!r}, c={c!r}"
    try:
        sides = sorted(float(side) for side in (a, b, c))
    except (TypeError, ValueError):
        log.exception(f"Нечисловые данные: {params}")
        return "", [(-2, -2)] * 3

    shortest, middle, longest = sides
    if not (shortest > 0 and shortest + middle > longest):
        log.error(f"Стороны не образуют треугольник: {params}")
        return "не треугольник", [(-1, -1)] * 3

    result = KINDS[len(set(sides))], vertices(*sides)
    log.info(f"Успех: {params} -> {result}")
    return result


def vertices(a: float, b: float, c: float) -> list[tuple[int, int]]:
    """Наибольшая сторона c лежит на оси X от (0, 0) до (FIELD_SIZE, 0), третья вершина — над ней."""
    a, b = a / c, b / c  # масштаб, при котором наибольшая сторона равна 1
    x = (1 + b * b - a * a) / 2
    y = math.sqrt(max(b * b - x * x, 0))
    return [(0, 0), (FIELD_SIZE, 0), (round(x * FIELD_SIZE), round(y * FIELD_SIZE))]
