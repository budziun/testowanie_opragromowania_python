import unittest
from src.bank import BankAccount

class TestBankAccount(unittest.TestCase):
    def test_deposit(self):
        account = BankAccount()
        account.deposit(100)
        self.assertEqual(account.get_balance(),100)
    def test_withdraw(self):
        account = BankAccount(200)
        account.withdraw(100)
        self.assertEqual(account.get_balance(),100)
    def test_negative_deposit(self):
        account = BankAccount()
        with self.assertRaises(ValueError):
            account.deposit(-10)
    def test_negative_withdraw(self):
        account = BankAccount()
        with self.assertRaises(ValueError):
            account.withdraw(-10)
    def test_withdraw_funds(self):
        account = BankAccount(50)
        with self.assertRaises(ValueError):
            account.withdraw(100)
    def test_initial_balance(self):
        account = BankAccount()
        self.assertEqual(account.get_balance(),500)
    def test_exact_withdraw(self):
        account = BankAccount(100)
        account.withdraw(100)
        self.assertEqual(account.get_balance(),0)
if __name__ == "__main__":
    unittest.main()