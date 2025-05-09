# System Zarządzania Restauracją

Kompleksowy system zarządzania restauracją zaimplementowany w Pythonie z testami jednostkowymi.

## Funkcjonalności

- Zarządzanie stanem magazynowym (składniki, przepisy, dostawy)
- Zarządzanie menu (dania, kategorie, dania dnia)
- Obsługa zamówień (tworzenie, przetwarzanie, rozliczanie)
- Śledzenie alergenów w daniach
- Monitorowanie stanów magazynowych i automatyczne generowanie listy zakupów
- Kalkulacja wartości magazynu

## Struktura Projektu

```
projekt/
├── src/
│   ├── __init__.py
│   ├── inventory_control.py   # Zarządzanie stanem magazynowym
│   ├── menu_management.py     # Zarządzanie menu
│   └── order_processing.py    # Obsługa zamówień
├── tests/
│   ├── __init__.py
│   ├── test_inventory_control.py
│   ├── test_menu_management.py
│   └── test_order_processing.py
└── README.md
```

## Instalacja

1. Sklonuj repozytorium
2. Brak dodatkowych zależności - projekt wykorzystuje standardową bibliotekę Pythona

## Uruchamianie Testów

Uruchom wszystkie testy za pomocą: `python -m unittest discover tests`

### Pokrycie Kodu

Projekt ma wysokie pokrycie kodu testami:

```
Name                              Stmts   Miss  Cover
-----------------------------------------------------
src\__init__.py                       0      0   100%
src\inventory_control.py            142      3    98%
src\menu_management.py               75      4    95%
src\order_processing.py             181      3    98%
tests\test_inventory_control.py     308      1    99%
tests\test_menu_management.py       221      1    99%
tests\test_order_processing.py      291      5    98%
-----------------------------------------------------
TOTAL                              1218     17    99%
```

Aby uruchomić testy z raportami pokrycia kodu:

1. Uruchom testy z coverage: `coverage run -m unittest discover tests`
2. Generuj raport w terminalu: `coverage report`

## Przykłady Użycia

### Zarządzanie stanem magazynowym

```python
from src.inventory_control import Skladnik, ZarzadzanieSkladnikami
from datetime import datetime, timedelta

# Utworzenie systemu zarządzania składnikami
system = ZarzadzanieSkladnikami()

# Dodawanie składników
maka = Skladnik("Mąka", "kg", 20, 5, 2.50)
mleko = Skladnik("Mleko", "l", 10, 3, 3.00, True)  # True - oznacza alergen
system.dodaj_skladnik(maka)
system.dodaj_skladnik(mleko)

# Dodawanie przepisu
system.dodaj_przepis("Naleśniki", {"Mąka": 0.5, "Mleko": 1.0})

# Przygotowanie dania (zużycie składników)
system.przygotuj_danie("Naleśniki", 2)  # 2 porcje

# Rejestracja dostawy
system.zarejestruj_dostawe("Dostawca X", {"Mąka": (10.0, 2.70), "Mleko": (5.0, 3.20)})

# Sprawdzenie stanu magazynu
print(f"Wartość magazynu: {system.oblicz_wartosc_magazynu()} PLN")
print(f"Lista do zamówienia: {[s.nazwa for s in system.lista_do_zamowienia()]}")
```

### Zarządzanie menu

```python
from src.menu_management import Danie, Menu

# Utworzenie menu
menu = Menu()

# Dodawanie dań
schabowy = Danie("Schabowy", 25.99, "danie główne", 20, 
                ["mięso wieprzowe", "bułka tarta", "jajko"], 
                {"gluten", "jajka"}, 450)
pomidorowa = Danie("Pomidorowa", 12.50, "zupa")
menu.dodaj_danie(schabowy)
menu.dodaj_danie(pomidorowa)

# Dodawanie dania dnia
menu.dodaj_danie_dnia("Schabowy")

# Wyszukiwanie dań
zupy = menu.znajdz_dania_po_kategorii("zupa")
tanie_dania = menu.znajdz_dania_w_cenie(10.0, 20.0)
```

### Obsługa zamówień

```python
from src.order_processing import ObslugaZamowien

# Inicjalizacja obsługi zamówień z referencją do menu
obsluga = ObslugaZamowien(menu)

# Utworzenie zamówienia
zamowienie = obsluga.utworz_zamowienie(5, "Jan")  # Stolik nr 5, kelner Jan

# Dodawanie pozycji do zamówienia
obsluga.dodaj_pozycje_do_zamowienia(zamowienie.id, "Schabowy", 2, "bez ziemniaków")
obsluga.dodaj_pozycje_do_zamowienia(zamowienie.id, "Pomidorowa", 1)

# Zmiana statusu zamówienia
zamowienie.zmien_status("w_realizacji")
zamowienie.zmien_status("dostarczone")

# Zamknięcie zamówienia (płatność)
kwota = obsluga.zamknij_zamowienie(zamowienie.id, "karta", 5.0)  # Metoda płatności, napiwek
print(f"Całkowita kwota do zapłaty: {kwota} PLN")

# Statystyki
print(f"Najpopularniejsze danie: {obsluga.statystyki['najpopularniejsze_danie']}")
print(f"Liczba zamówień: {obsluga.statystyki['liczba_zamowien']}")
```

## Funkcje Modułów

### inventory_control.py
- `Skladnik` - Klasa reprezentująca składnik używany w restauracji
- `ZarzadzanieSkladnikami` - Klasa zarządzająca wszystkimi składnikami i przepisami

### menu_management.py
- `Danie` - Klasa reprezentująca pojedyncze danie w menu restauracji
- `Menu` - Klasa reprezentująca całe menu restauracji

### order_processing.py
- `PozycjaZamowienia` - Klasa reprezentująca pojedynczą pozycję w zamówieniu
- `Zamowienie` - Klasa reprezentująca całe zamówienie
- `ObslugaZamowien` - Klasa zarządzająca wszystkimi zamówieniami w restauracji

Plik README.md wygenerowano przy użyciu Claude.AI. - model Claude 3.7 Sonnet [https://claude.ai]