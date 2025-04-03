import unittest
from src.sport import Sport

class TestSportInitialization(unittest.TestCase):
    def setUp(self):
        pass
    def test_create_sport_object(self):
        sport = Sport("Running",30)
        self.assertIsInstance(sport,Sport)
    def test_asttributes_assignment(self):
        sport = Sport("Running",30)
        self.assertEqual(sport.name,"Running")
        self.assertEqual(sport.duration,30)
    def test_empty_name_raises_value_error(self):
        with self.assertRaises(ValueError):
            Sport("", 30)
    def test_numeric_name_raises_type_error(self):
        with self.assertRaises(TypeError):
            Sport(123, 30)
    def test_zero_duration_raises_value_error(self):
        with self.assertRaises(ValueError):
            Sport("Running", 0)
    def test_negative_duration_raises_value_error(self):
        with self.assertRaises(ValueError):
            Sport("Running", -5)
    def test_string_duration_raises_type_error(self):
        with self.assertRaises(TypeError):
            Sport("Running", "thirty")
    def test_calculate_calories_running(self):
        sport = Sport("Running", 30)
        self.assertEqual(sport.calculate_calories(), 300)
    def test_calculate_calories_swimming(self):
        sport = Sport("Swimming", 45)
        self.assertEqual(sport.calculate_calories(), 450)
    def tearDown(self):
        pass

if __name__ == "__main__":
    unittest.main()