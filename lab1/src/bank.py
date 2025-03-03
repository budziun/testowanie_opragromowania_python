class InsufficientFundsError(Exception):
    pass
class BankAccount:
    def __init__(self,balance=0.0):
        self.balance = balance
    def deposit(self,amount: float):
        if amount <0:
            raise ValueError("Nie możesz wpłacić kwoty mniejszej niz 0")
        self.balance += amount
    def withdraw(self,amount: float):
        if amount < 0:
            raise ValueError("Nie możesz wypłacić kwoty mniejszej niż 0")
        if amount > self.balance:
            raise InsufficientFundsError("Brak wystarczających funfuszy na koncie do wypłaty")
        self.balance -= amount
    def get_balance(self) -> float:
        return self.balance