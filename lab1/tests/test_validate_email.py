import unittest
from src.mail import validate_email


class TestValidateEmail(unittest.TestCase):
    def test_valid_emails(self):
        self.assertTrue(validate_email("test@gmail.com"))
        self.assertTrue(validate_email("user.name+tag@domain.co.uk"))
        self.assertTrue(validate_email("12345@sub.onet.com"))

    def test_missing_at_symbol(self):
        self.assertFalse(validate_email("test.gmail.com"))
        self.assertFalse(validate_email("123#wp.pl"))

    def test_missing_domain(self):
        self.assertFalse(validate_email("test@.com"))
        self.assertFalse(validate_email("test@test"))

    def test_missing_local_part(self):
        self.assertFalse(validate_email("@gmail.com"))
        self.assertFalse(validate_email("@.ccom"))

    def test_invalid_characters(self):
        self.assertFalse(validate_email("123@gmail,com"))
        self.assertFalse(validate_email("123@gmail@wp@com"))
        self.assertFalse(validate_email("321@onet,..com"))

    def test_empty_string(self):
        self.assertFalse(validate_email(""))


if __name__ == "__main__":
    unittest.main()
