import unittest
from src.temperatura import TemperatureConverter

class TestTemperatureConventer(unittest.TestCase):
    def test_celsius_to_fahrenheit(self):
        self.assertAlmostEqual(TemperatureConverter.celsius_to_fahrenheit(0), 32)
        self.assertAlmostEqual(TemperatureConverter.celsius_to_fahrenheit(100), 212)
        self.assertAlmostEqual(TemperatureConverter.celsius_to_fahrenheit(-40), -40)
    def test_fahrenheit_to_celsius(self):
        self.assertAlmostEqual(TemperatureConverter.fahrenheit_to_celsius(32),0)
        self.assertAlmostEqual(TemperatureConverter.fahrenheit_to_celsius(212),100)
        self.assertAlmostEqual(TemperatureConverter.fahrenheit_to_celsius(-40),-40)
    def test_celsius_to_kelvin(self):
        self.assertAlmostEqual(TemperatureConverter.celsius_to_kelvin(0),273.15)
        self.assertAlmostEqual(TemperatureConverter.celsius_to_kelvin(100),373.15)
    def test_kelvin_to_celsius(self):
        self.assertAlmostEqual(TemperatureConverter.kelvin_to_celsius(273.15),0)
        self.assertAlmostEqual(TemperatureConverter.kelvin_to_celsius(400),100)
if __name__ == "__main__":
    unittest.main()