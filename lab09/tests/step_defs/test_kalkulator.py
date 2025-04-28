import pytest
from pytest_bdd import scenarios, given, when, then, parsers
from src.kalkulator import Kalkulator

# Ładowanie scenariuszy z pliku .feature
scenarios('../features/kalkulator.feature')

# Fixture kalkulatora
@pytest.fixture
def kalkulator():
    return Kalkulator()

# Wspólny krok dla wszystkich scenariuszy
@given('kalkulator', target_fixture='kalkulator')
def mam_kalkulator():
    return Kalkulator()

# Implementacja kroków
@when(parsers.parse('wprowadzę liczbę {liczba:d}'))
@when(parsers.parse('wprowadzę liczbę {liczba:f}'))
def wprowadz_liczbe(kalkulator, liczba):
    if kalkulator.liczba1 is None:
        kalkulator.wprowadz_liczbe1(liczba)
    else:
        kalkulator.wprowadz_liczbe2(liczba)

@when('wybiorę operację dodawania')
def wybierz_dodawanie(kalkulator):
    kalkulator.dodaj()

@when('wybiorę operację odejmowania')
def wybierz_odejmowanie(kalkulator):
    kalkulator.odejmij()

@when('wybiorę operację mnożenia')
def wybierz_mnozenie(kalkulator):
    kalkulator.pomnoz()

@when('wybiorę operację dzielenia')
def wybierz_dzielenie(kalkulator):
    kalkulator.podziel()

@then(parsers.parse('wynik powinien wynosić {oczekiwany_wynik:d}'))
@then(parsers.parse('wynik powinien wynosić {oczekiwany_wynik:f}'))
def sprawdz_wynik(kalkulator, oczekiwany_wynik):
    assert kalkulator.pobierz_wynik() == float(oczekiwany_wynik)

@then(parsers.parse('powinien zostać zgłoszony błąd "{oczekiwany_blad}"'))
def sprawdz_blad(kalkulator, oczekiwany_blad):
    assert kalkulator.pobierz_blad() == oczekiwany_blad