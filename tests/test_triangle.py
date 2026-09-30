import logging
import unittest

from src.triangle import get_triangle, log

NOT_TRIANGLE = ("не треугольник", [(-1, -1)] * 3)
INVALID = ("", [(-2, -2)] * 3)

log.addHandler(logging.NullHandler())  # чтобы логи не засоряли вывод тестов


class TestTriangleKind(unittest.TestCase):
    def test_equal_sides_is_equilateral(self):
        self.assertEqual(get_triangle("3", "3", "3")[0], "равносторонний")

    def test_two_equal_sides_is_isosceles_in_any_order(self):
        for sides in [("5", "5", "8"), ("5", "8", "5"), ("8", "5", "5")]:
            with self.subTest(sides=sides):
                self.assertEqual(get_triangle(*sides)[0], "равнобедренный")

    def test_different_sides_is_scalene(self):
        self.assertEqual(get_triangle("3", "4", "5")[0], "разносторонний")

    def test_fractional_and_scientific_notation_are_accepted(self):
        self.assertEqual(get_triangle("2.5", "2.50", "25e-1")[0], "равносторонний")


class TestNotTriangle(unittest.TestCase):
    def test_degenerate_triangle_is_not_triangle(self):
        self.assertEqual(get_triangle("1", "2", "3"), NOT_TRIANGLE)

    def test_side_longer_than_sum_of_others_is_not_triangle(self):
        self.assertEqual(get_triangle("1", "2", "10"), NOT_TRIANGLE)

    def test_zero_side_is_not_triangle(self):
        self.assertEqual(get_triangle("0", "1", "1"), NOT_TRIANGLE)

    def test_negative_side_is_not_triangle(self):
        self.assertEqual(get_triangle("-3", "4", "5"), NOT_TRIANGLE)


class TestInvalidInput(unittest.TestCase):
    def test_text_is_invalid(self):
        self.assertEqual(get_triangle("abc", "4", "5"), INVALID)

    def test_empty_string_is_invalid(self):
        self.assertEqual(get_triangle("", "4", "5"), INVALID)

    def test_comma_decimal_separator_is_invalid(self):
        self.assertEqual(get_triangle("3,5", "4", "5"), INVALID)

    def test_none_is_invalid(self):
        self.assertEqual(get_triangle(None, "4", "5"), INVALID)

    def test_nan_is_invalid(self):
        self.assertEqual(get_triangle("nan", "1", "1"), INVALID)

    def test_infinity_is_invalid(self):
        self.assertEqual(get_triangle("inf", "1", "1"), INVALID)

    def test_invalid_input_has_priority_over_not_triangle(self):
        self.assertEqual(get_triangle("-1", "abc", "5"), INVALID)


class TestVertices(unittest.TestCase):
    def test_equilateral_vertices(self):
        self.assertEqual(get_triangle("1", "1", "1")[1], [(0, 0), (99, 0), (50, 86)])

    def test_right_triangle_vertices(self):
        self.assertEqual(get_triangle("3", "4", "5")[1], [(0, 0), (99, 0), (63, 48)])

    def test_vertices_fit_in_100x100_field(self):
        for sides in [("1", "1", "1"), ("3", "4", "5"), ("1", "1", "1.99"), ("1000", "1", "1000")]:
            for x, y in get_triangle(*sides)[1]:
                with self.subTest(sides=sides, vertex=(x, y)):
                    self.assertTrue(0 <= x < 100 and 0 <= y < 100)

    def test_vertices_do_not_depend_on_scale(self):
        self.assertEqual(get_triangle("3", "4", "5")[1], get_triangle("300", "400", "500")[1])

    def test_vertices_do_not_depend_on_side_order(self):
        self.assertEqual(get_triangle("3", "4", "5")[1], get_triangle("5", "3", "4")[1])


class TestLogging(unittest.TestCase):
    def test_success_is_logged_as_info(self):
        with self.assertLogs(log, "INFO") as logs:
            get_triangle("3", "4", "5")
        self.assertEqual(logs.records[0].levelname, "INFO")

    def test_invalid_input_is_logged_as_error_with_traceback(self):
        with self.assertLogs(log, "ERROR") as logs:
            get_triangle("abc", "4", "5")
        self.assertIsNotNone(logs.records[0].exc_info)


if __name__ == "__main__":
    unittest.main()
