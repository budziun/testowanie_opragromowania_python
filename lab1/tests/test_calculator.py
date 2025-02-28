import unittest
from src.Calculator import Calculator

class TestCalculator(unittest.TestCase):
    def setUp(self):
        self.calc = Calculator()
    def test_add(self):
        self.assertEqual(self.calc.add(2,3),5)
        self.assertEqual(self.calc.add(-1,1),0)
        self.assertEqual(self.calc.add(2,2),5)
    def test_subtract(self):
        self.assertEqual(self.calc.subtract(5,4),1)
        self.assertEqual(self.calc.subtract(4,-2),6)
        self.assertEqual(self.calc.subtract(2,1),5)
    def test_multiply(self):
        self.assertEqual(self.calc.multiply(2,2),4)
        self.assertEqual(self.calc.multiply(-2,-2),4)
        self.assertEqual(self.calc.multiply(-2,10),20)
    def test_divide(self):
        self.assertEqual(self.calc.divide(4,2),2)
    def test_divdie_by_zero(self):
        with self.assertRaises(ZeroDivisionError):
            self.calc.divide(10,0)

    def tearDown(self):
        pass
if __name__ == "__main__":
    unittest.main()