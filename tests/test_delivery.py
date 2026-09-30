import unittest

from src.delivery import calculate_delivery_cost

ERROR = (-1, "0000-00-00")  # дата отправки в модуле зафиксирована: 2026-09-03


class TestValidation(unittest.TestCase):
    def test_min_weight_is_accepted(self):
        self.assertNotEqual(calculate_delivery_cost(0.1, 100, "обычный"), ERROR)

    def test_max_weight_is_accepted(self):
        self.assertNotEqual(calculate_delivery_cost(50.0, 100, "обычный"), ERROR)

    def test_weight_below_min_is_rejected(self):
        self.assertEqual(calculate_delivery_cost(0.09, 100, "обычный"), ERROR)

    def test_weight_above_max_is_rejected(self):
        self.assertEqual(calculate_delivery_cost(50.01, 100, "обычный"), ERROR)

    def test_min_distance_is_accepted(self):
        self.assertNotEqual(calculate_delivery_cost(1.0, 1, "обычный"), ERROR)

    def test_max_distance_is_accepted(self):
        self.assertNotEqual(calculate_delivery_cost(1.0, 5000, "обычный"), ERROR)

    def test_zero_distance_is_rejected(self):
        self.assertEqual(calculate_delivery_cost(1.0, 0, "обычный"), ERROR)

    def test_distance_above_max_is_rejected(self):
        self.assertEqual(calculate_delivery_cost(1.0, 5001, "обычный"), ERROR)

    def test_unknown_package_type_is_rejected(self):
        self.assertEqual(calculate_delivery_cost(1.0, 100, "стеклянный"), ERROR)

    def test_non_numeric_weight_is_rejected_without_crash(self):
        self.assertEqual(calculate_delivery_cost("abc", 100, "обычный"), ERROR)


class TestCost(unittest.TestCase):
    def test_base_cost_is_200_plus_5_per_km(self):
        self.assertEqual(calculate_delivery_cost(1.0, 100, "обычный")[0], 700)

    def test_weight_up_to_5kg_has_no_markup(self):
        self.assertEqual(calculate_delivery_cost(5.0, 100, "обычный")[0], 700)

    def test_weight_over_5kg_adds_20_percent(self):
        self.assertEqual(calculate_delivery_cost(10.0, 100, "обычный")[0], 840)

    def test_weight_from_20kg_adds_50_percent(self):
        self.assertEqual(calculate_delivery_cost(20.0, 100, "обычный")[0], 1050)

    def test_fragile_package_adds_300(self):
        self.assertEqual(calculate_delivery_cost(1.0, 100, "хрупкий")[0], 1000)

    def test_dangerous_package_adds_1000(self):
        self.assertEqual(calculate_delivery_cost(1.0, 100, "опасный")[0], 1700)

    def test_express_costs_more_than_regular(self):
        regular = calculate_delivery_cost(1.0, 100, "обычный")[0]
        express = calculate_delivery_cost(1.0, 100, "обычный", is_express=True)[0]
        self.assertGreater(express, regular)


class TestDeliveryDate(unittest.TestCase):
    def test_short_distance_takes_one_day(self):
        self.assertEqual(calculate_delivery_cost(1.0, 1, "обычный")[1], "2026-09-04")

    def test_each_500_km_takes_one_day(self):
        self.assertEqual(calculate_delivery_cost(1.0, 1000, "обычный")[1], "2026-09-05")

    def test_started_500_km_counts_as_full_day(self):
        self.assertEqual(calculate_delivery_cost(1.0, 501, "обычный")[1], "2026-09-05")

    def test_express_halves_delivery_time(self):
        self.assertEqual(calculate_delivery_cost(1.0, 2000, "обычный", is_express=True)[1], "2026-09-05")

    def test_express_is_not_delivered_on_shipping_day(self):
        self.assertEqual(calculate_delivery_cost(1.0, 100, "обычный", is_express=True)[1], "2026-09-04")


if __name__ == "__main__":
    unittest.main()
