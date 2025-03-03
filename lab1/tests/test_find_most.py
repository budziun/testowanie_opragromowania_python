import unittest
from src.find_most import find_most_frequent_word

class TestFindMostFrequentWord(unittest.TestCase):
    def test_empty_text(self):
        self.assertEqual(find_most_frequent_word(""),"")
    def test_single_word(self):
        self.assertEqual(find_most_frequent_word("hello"),"hello")
    def test_muli_words(self):
        self.assertEqual(find_most_frequent_word("piwo perła piwo"),"piwo")
    def test_tie(self):
        result = find_most_frequent_word("piwo lubie piwo lubie")
        self.assertIn(result,["piwo","perła"])
    def test_case_insensitivity(self):
        self.assertEqual(find_most_frequent_word("Hello hello HELLO"),"hello")
if __name__ == "__main__":
    unittest.main()