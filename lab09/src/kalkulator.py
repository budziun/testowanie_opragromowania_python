class Kalkulator:
    def __init__(self):
        self.liczba1 = None
        self.liczba2 = None
        self.wynik = None
        self.error = None

    def wprowadz_liczbe1(self, liczba):
        self.liczba1 = float(liczba)

    def wprowadz_liczbe2(self, liczba):
        self.liczba2 = float(liczba)

    def dodaj(self):
        self.wynik = self.liczba1 + self.liczba2

    def odejmij(self):
        self.wynik = self.liczba1 - self.liczba2

    def pomnoz(self):
        self.wynik = self.liczba1 * self.liczba2

    def podziel(self):
        try:
            self.wynik = self.liczba1 / self.liczba2
        except ZeroDivisionError:
            self.error = "Nie można dzielić przez zero"

    def pobierz_wynik(self):
        return self.wynik

    def pobierz_blad(self):
        return self.error