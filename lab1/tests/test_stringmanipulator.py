import unittest
from src.stringman import StringManipulator

class TestStringManipulator(unittest.TestCase):
    def setUp(self):
        self.manipulator = StringManipulator()

    def test_reverse_string(self):
        self.assertEqual(self.manipulator.reverse_string("hej"),"jeh")
        self.assertEqual(self.manipulator.reverse_string("Budziun"),"nuizduB")
        self.assertEqual(self.manipulator.reverse_string("123"),"3210")
        self.assertEqual(self.manipulator.reverse_string(""),"")
    def test_count_words(self):
        self.assertEqual(self.manipulator.count_words("hello piojas"),2)
        self.assertEqual(self.manipulator.count_words("lubie pic piwo"),3)
        self.assertEqual(self.manipulator.count_words(""),0)
        self.assertEqual(self.manipulator.count_words("Jestem w mega gazie"),5)
    def test_capitalize_words(self):
        self.assertEqual(self.manipulator.capitalize_words("hello world"), "Hello World")
        self.assertEqual(self.manipulator.capitalize_words("szybki test tego typu"), "Szybki Test Tego Typu")
        self.assertEqual(self.manipulator.capitalize_words(""),"")
        self.assertEqual(self.manipulator.capitalize_words("123 abcdefg"),"123 abcdefg")

if __name__ == "__main__":
    unittest.main()