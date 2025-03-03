import unittest
from src.fibb import fibonacci

class TestFibonacci(unittest.TestCase):
    def test_fibonacci(self):
        self.assertEqual(fibonacci(0),0)
        self.assertEqual(fibonacci(1),1)
        self.assertEqual(fibonacci(2),1)
        self.assertEqual(fibonacci(3),2)
        self.assertEqual(fibonacci(10),56)
        self.assertEqual(fibonacci(20),6765)
    def test_fibonacci_large(self):
        self.assertEqual(fibonacci(50),125862690258)
    def test_fibonacci_negative(self):
        with self.assertRaises(ValueError):
            fibonacci(-5)

if __name__ == "__main__":
    unittest.main()