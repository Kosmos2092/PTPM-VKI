import unittest

from src.converter import Converter


class TestFrom100_7ToInfinity(unittest.TestCase):
    def test_lower_bound_100_7_returns_1000(self):
        self.assertEqual(Converter.do(100.7), 1000)

    def test_big_number_returns_1000(self):
        self.assertEqual(Converter.do(5000.5), 1000)


class TestFromZeroTo100_7(unittest.TestCase):
    def test_just_below_100_7_returns_integer_part(self):
        self.assertEqual(Converter.do(100.6), 100)

    def test_just_above_zero_returns_integer_part(self):
        self.assertEqual(Converter.do(0.1), 0)

    def test_middle_value_drops_fraction(self):
        self.assertEqual(Converter.do(65.7), 65)


class TestZero(unittest.TestCase):
    def test_zero_raises_value_error(self):
        with self.assertRaises(ValueError):
            Converter.do(0.0)

    def test_negative_zero_raises_value_error(self):
        with self.assertRaises(ValueError):
            Converter.do(-0.0)


class TestFromMinus30_4ToZero(unittest.TestCase):
    def test_just_below_zero_returns_integer_part_minus_5(self):
        self.assertEqual(Converter.do(-0.1), -5)

    def test_lower_bound_minus_30_4_returns_integer_part_minus_5(self):
        self.assertEqual(Converter.do(-30.4), -35)

    def test_middle_value_returns_integer_part_minus_5(self):
        self.assertEqual(Converter.do(-10.3), -15)


class TestFromMinusInfinityToMinus30_5(unittest.TestCase):
    def test_upper_bound_minus_30_5_returns_minus_2000(self):
        self.assertEqual(Converter.do(-30.5), -2000)

    def test_big_negative_number_returns_minus_2000(self):
        self.assertEqual(Converter.do(-94.5), -2000)


class TestResultType(unittest.TestCase):
    def test_result_is_int_in_every_range(self):
        for x in [100.7, 65.7, -10.3, -94.5]:
            with self.subTest(x=x):
                self.assertIsInstance(Converter.do(x), int)


if __name__ == "__main__":
    unittest.main()
