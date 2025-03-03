import unittest
from src.palindrom import is_palindrome

class TestIsPalindrome(unittest.TestCase):
    def test_simple_palindromes(self):
        self.assertTrue(is_palindrome("anna"))
        self.assertTrue(is_palindrome("kajak"))
        self.assertTrue(is_palindrome("12321"))
    def test_palindrome_with_space(self):
        self.assertTrue(is_palindrome("Kajak kajaK"))
        self.assertTrue(is_palindrome("No 'x' in Nixon"))
    def test_non_palindromes(self):
        self.assertFalse(is_palindrome("Piwo"))
        self.assertFalse(is_palindrome("123456"))
    def test_case_insensitivity(self):
        self.assertTrue(is_palindrome("aNnA"))
        self.assertTrue(is_palindrome("kaJaK"))
    def test_empty(self):
        self.assertTrue(is_palindrome(""))
    def test_single_char(self):
        self.assertTrue(is_palindrome("ą"))
if __name__ == "__main__":
    unittest.main()