"""
Testy jednostkowe dla modułu menu_management.
Testowane są klasy Danie i Menu oraz wszystkie ich metody.

Częściowo wygenerowano przy użyciu Claude.ai
model Claude 3.7 Sonnet
"""
import unittest
from datetime import datetime, timedelta
from src.menu_management import Danie, Menu


class TestDanieInit(unittest.TestCase):
    """
    Testy dla klasy Danie.
    """

    def test_init_with_required_params(self):
        """Test inicjalizacji z wymaganymi parametrami."""
        danie = Danie("Schabowy", 25.99, "danie główne")
        self.assertEqual(danie.nazwa, "Schabowy")
        self.assertEqual(danie.cena, 25.99)
        self.assertEqual(danie.kategoria, "danie główne")
        self.assertEqual(danie.czas_przygotowania, 30)
        self.assertTrue(danie.dostepne)
        self.assertCountEqual(danie.skladniki, [])
        self.assertIsNone(danie.kalorie)

    def test_init_with_all_params(self):
        """
        Test inicjalizacji ze wszystkimi parametrami.
        W tym przykładzie dodano składniki co nie jest wymaganym działaniem
        """
        skladniki = ["mięso wieprzowe", "bułka tarta", "jajko"]
        danie = Danie("Schabowy", 25.99, "danie główne", 20, skladniki, 450)
        self.assertEqual(danie.nazwa, "Schabowy")
        # Używamy assertNotEqual aby podkreślić, że cena nie jest domyślna
        self.assertNotEqual(danie.cena, 0)
        self.assertEqual(danie.kategoria, "danie główne")
        # Używamy assertLess aby sprawdzić,
        # czy czas przygotowania jest mniejszy od domyślnego
        self.assertLess(danie.czas_przygotowania, 30)
        self.assertTrue(danie.dostepne)
        # Używamy assertCountEqual zamiast assertEqual dla listy składników
        self.assertCountEqual(danie.skladniki, skladniki)
        self.assertEqual(danie.kalorie, 450)
        # Dodajemy assertIsInstance dla sprawdzenia typu daty dodania
        self.assertIsInstance(danie.data_dodania, datetime)

    def test_init_negative_price(self):
        """Test inicjalizacji z ujemną ceną."""
        with self.assertRaises(ValueError):
            Danie("Schabowy", -5.0, "danie główne")

    def test_init_zero_price(self):
        """Test inicjalizacji z ceną równą zero."""
        with self.assertRaises(ValueError):
            Danie("Schabowy", 0, "danie główne")

    def test_init_price_validation_message(self):
        """Test sprawdzający komunikat błędu przy ujemnej cenie."""
        # Używamy assertRaisesRegex aby sprawdzić treść komunikatu błędu
        with self.assertRaisesRegex(ValueError,
                                    "Cena dania musi być większa od zera"):
            Danie("Schabowy", -5.0, "danie główne")


class TestDanieMetody(unittest.TestCase):
    """
    Testy metod klasy Danie.
    """

    def setUp(self):
        """Przygotowanie danych do testów."""
        self.danie = Danie("Schabowy", 25.99, "danie główne", 20,
                           ["mięso wieprzowe", "bułka tarta", "jajko"], 450)
        # Dodatkowe danie dla testów porównawczych
        self.tanie_danie = Danie("Frytki", 8.50,
                                 "dodatek", 10, ["ziemniaki"], 300)

    def test_zmien_cene_valid(self):
        """Test zmiany ceny."""
        stara_cena = self.danie.cena
        self.danie.zmien_cene(30.50)
        self.assertEqual(self.danie.cena, 30.50)
        # Sprawdzamy czy nowa cena jest większa od starej
        self.assertGreater(self.danie.cena, stara_cena)

    def test_zmien_cene_negative(self):
        """Test zmiany ceny na ujemną wartość."""
        with self.assertRaises(ValueError):
            self.danie.zmien_cene(-10.0)

    def test_zmien_cene_zero(self):
        """Test zmiany ceny na zero."""
        with self.assertRaises(ValueError):
            self.danie.zmien_cene(0)

    def test_ustaw_dostepnosc_true(self):
        """Test ustawienia dostępności na dostępne (True)."""
        self.danie.ustaw_dostepnosc(True)
        self.assertTrue(self.danie.dostepne)

    def test_ustaw_dostepnosc_false(self):
        """Test ustawienia dostępności na niedostępne (False)."""
        self.danie.ustaw_dostepnosc(False)
        self.assertFalse(self.danie.dostepne)
        # Sprawdzamy że po ustawieniu na False, atrybut nie jest None
        self.assertIsNotNone(self.danie.dostepne)

    def test_dodaj_skladnik_new(self):
        """Test dodania nowego składnika."""
        # Zapamiętujemy rozmiar przed dodaniem
        poczatkowa_liczba_skladnikow = len(self.danie.skladniki)
        self.danie.dodaj_skladnik("sól")
        self.assertIn("sól", self.danie.skladniki)
        # Sprawdzamy czy liczba składników zwiększyła się o 1
        self.assertEqual(len(self.danie.skladniki),
                         poczatkowa_liczba_skladnikow + 1)
        # Używamy assertGreater zamiast assertEqual
        self.assertGreater(len(self.danie.skladniki),
                           poczatkowa_liczba_skladnikow)

    def test_dodaj_skladnik_existing(self):
        """Test dodania istniejącego składnika."""
        # Używamy assertRaisesRegex zamiast assertRaises
        with self.assertRaisesRegex(ValueError,
                                    r"Składnik .* już jest częścią dania"):
            # Składnik już znajduje się w daniu
            # ("mięso wieprzowe", "bułka tarta", "jajko")
            self.danie.dodaj_skladnik("jajko")

    def test_usun_skladnik_existing(self):
        """Test usunięcia istniejącego składnika."""
        # składniki przed usunięciem ("mięso wieprzowe","bułka tarta","jajko")
        poczatkowa_liczba_skladnikow = len(self.danie.skladniki)
        self.danie.usun_skladnik("jajko")
        # składniki po usunięciu ("mięso wieprzowe", "bułka tarta")
        self.assertNotIn("jajko", self.danie.skladniki)
        # Używamy assertLess zamiast assertEqual
        self.assertLess(len(self.danie.skladniki),
                        poczatkowa_liczba_skladnikow)

    def test_usun_skladnik_non_existing(self):
        """Test usunięcia nieistniejącego składnika."""
        with self.assertRaisesRegex(ValueError,
                                    r"Składnik .* nie jest częścią dania"):
            self.danie.usun_skladnik("sól")

    def test_compare_prices(self):
        """Test porównujący ceny różnych dań."""
        # Używamy assertGreater do porównania cen
        self.assertGreater(self.danie.cena, self.tanie_danie.cena)
        self.assertLess(self.tanie_danie.cena, self.danie.cena)
        # Używamy assertGreaterEqual, nawet jeśli wiemy, że są różne
        self.assertGreaterEqual(self.danie.cena, self.tanie_danie.cena)
        # Używamy assertLessEqual
        self.assertLessEqual(self.tanie_danie.cena, self.danie.cena)


class TestMenuInit(unittest.TestCase):
    """
    Testy inicjalizacji klasy Menu.
    """

    def test_init_default(self):
        """Test inicjalizacji z domyślnymi parametrami."""
        menu = Menu()
        self.assertEqual(menu.dania, {})
        # Używamy assertIsInstance zamiast assertEqual dla zbiorów
        self.assertIsInstance(menu.kategorie, set)
        self.assertEqual(menu.dania_dnia, [])
        self.assertEqual(menu.max_dania_dnia, 3)
        self.assertIsInstance(menu.data_aktualizacji, datetime)
        # Sprawdzamy czy data aktualizacji jest nie starsza niż 1 minuta
        minuta_temu = datetime.now() - timedelta(minutes=1)
        self.assertGreaterEqual(menu.data_aktualizacji, minuta_temu)

    def test_init_custom_max_dania(self):
        """Test inicjalizacji z własną maksymalną liczbą dań dnia."""
        menu = Menu(max_dania_dnia=5)
        self.assertEqual(menu.max_dania_dnia, 5)
        # Używamy assertGreater do sprawdzenia wartości parametru
        self.assertGreater(menu.max_dania_dnia, 3)

    def test_init_negative_max_dania(self):
        """Test inicjalizacji z ujemną maksymalną liczbą dań dnia."""
        with self.assertRaisesRegex(ValueError,
                                    r"Maksymalna liczba dań dnia musi być"
                                    r" większa od 0"):
            Menu(max_dania_dnia=-1)

    def test_init_zero_max_dania(self):
        """Test inicjalizacji z maksymalną liczbą dań dnia równą zero."""
        with self.assertRaisesRegex(ValueError,
                                    r"Maksymalna liczba dań dnia "
                                    r"musi być większa od 0"):
            Menu(max_dania_dnia=0)


class TestMenuDodajUsunDanie(unittest.TestCase):
    """
    Testy metod dodaj_danie i usun_danie klasy Menu.
    """

    def setUp(self):
        """Przygotowanie danych do testów."""
        self.menu = Menu()
        self.danie1 = Danie("Schabowy", 25.99, "danie główne")
        self.danie2 = Danie("Pomidorowa", 12.50, "zupa")
        self.danie3 = Danie("Tiramisu", 15.00, "deser")

    def test_dodaj_danie_single(self):
        """Test dodania pojedynczego dania."""
        self.menu.dodaj_danie(self.danie1)
        self.assertIn("Schabowy", self.menu.dania)
        # Używamy assertIs zamiast assertEqual
        # aby sprawdzić identyczność obiektów
        self.assertIs(self.menu.dania["Schabowy"], self.danie1)
        self.assertEqual(len(self.menu.dania), 1)
        self.assertIn("danie główne", self.menu.kategorie)

    def test_dodaj_danie_multiple(self):
        """Test dodania wielu dań."""
        self.menu.dodaj_danie(self.danie1)
        self.menu.dodaj_danie(self.danie2)
        self.menu.dodaj_danie(self.danie3)

        self.assertEqual(len(self.menu.dania), 3)
        # Używamy assertCountEqual do sprawdzenia
        # zawartości zbioru (bez względu na kolejność)
        self.assertCountEqual(self.menu.kategorie,
                              {"danie główne", "zupa", "deser"})
        self.assertIn("Schabowy", self.menu.dania)
        self.assertIn("Pomidorowa", self.menu.dania)
        self.assertIn("Tiramisu", self.menu.dania)

        # Sprawdzamy, czy wszystkie kategorie zostały poprawnie dodane
        for kategoria in ["danie główne", "zupa", "deser"]:
            self.assertIn(kategoria, self.menu.kategorie)

    def test_dodaj_danie_duplicate(self):
        """Test dodania dania o istniejącej nazwie."""
        self.menu.dodaj_danie(self.danie1)

        danie_duplicate = Danie("Schabowy", 30.00, "danie główne")
        with self.assertRaisesRegex(ValueError,
                                    r"Danie o nazwie .* już istnieje w menu"):
            self.menu.dodaj_danie(danie_duplicate)

    def test_usun_danie_existing(self):
        """Test usunięcia istniejącego dania."""
        self.menu.dodaj_danie(self.danie1)
        self.menu.dodaj_danie(self.danie2)

        # Zapamiętujemy liczbę dań i kategorii przed usunięciem
        liczba_dan_przed = len(self.menu.dania)
        kategorie_przed = set(self.menu.kategorie)

        self.menu.usun_danie("Schabowy")

        self.assertNotIn("Schabowy", self.menu.dania)
        # Używamy assertLess zamiast assertEqual
        self.assertLess(len(self.menu.dania), liczba_dan_przed)
        # Sprawdzamy, że kategoria została usunięta
        self.assertNotIn("danie główne", self.menu.kategorie)
        # Sprawdzamy, że zbiór kategorii się zmienił
        self.assertNotEqual(self.menu.kategorie, kategorie_przed)

    def test_usun_danie_non_existing(self):
        """Test usunięcia nieistniejącego dania."""
        with self.assertRaisesRegex(KeyError,
                                    r"Danie o nazwie .* nie istnieje w menu"):
            self.menu.usun_danie("Nieistniejące danie")


class TestMenuDanieDnia(unittest.TestCase):
    """
    Testy metod związanych z daniami dnia.
    """

    def setUp(self):
        """Przygotowanie danych do testów."""
        self.menu = Menu(max_dania_dnia=2)
        self.danie1 = Danie("Schabowy", 25.99, "danie główne")
        self.danie2 = Danie("Pomidorowa", 12.50, "zupa")
        self.danie3 = Danie("Tiramisu", 15.00, "deser")

        self.menu.dodaj_danie(self.danie1)
        self.menu.dodaj_danie(self.danie2)
        self.menu.dodaj_danie(self.danie3)

    def test_dodaj_danie_dnia_single(self):
        """Test dodania pojedynczego dania dnia."""
        self.menu.dodaj_danie_dnia("Schabowy")
        # Używamy assertLessEqual zamiast assertEqual
        self.assertLessEqual(len(self.menu.dania_dnia),
                             self.menu.max_dania_dnia)
        self.assertIn(self.danie1, self.menu.dania_dnia)
        # Sprawdzamy czy obiekt w dania_dnia
        # jest identyczny z oryginalnym obiektem
        self.assertIs(self.menu.dania_dnia[0], self.danie1)

    def test_dodaj_danie_dnia_multiple(self):
        """Test dodania wielu dań dnia."""
        self.menu.dodaj_danie_dnia("Schabowy")
        self.menu.dodaj_danie_dnia("Pomidorowa")

        # Używamy assertEqual z dokładnym porównaniem liczby dań
        self.assertEqual(len(self.menu.dania_dnia), 2)
        self.assertIn(self.danie1, self.menu.dania_dnia)
        self.assertIn(self.danie2, self.menu.dania_dnia)
        # Sprawdzamy, czy liczba dań dnia osiągnęła maksymalną wartość
        self.assertEqual(len(self.menu.dania_dnia), self.menu.max_dania_dnia)

    def test_dodaj_danie_dnia_too_many(self):
        """Test próby dodania większej liczby dań dnia niż limit."""
        self.menu.dodaj_danie_dnia("Schabowy")
        self.menu.dodaj_danie_dnia("Pomidorowa")

        # Używamy assertRaisesRegex aby sprawdzić dokładny komunikat błędu
        with self.assertRaisesRegex(ValueError, r"Lista dań dnia jest pełna"):
            self.menu.dodaj_danie_dnia("Tiramisu")

    def test_usun_danie_dnia_existing(self):
        """Test usunięcia istniejącego dania dnia."""
        self.menu.dodaj_danie_dnia("Schabowy")
        self.menu.dodaj_danie_dnia("Pomidorowa")

        # Zapamiętujemy liczbę dań dnia przed usunięciem
        liczba_dan_dnia_przed = len(self.menu.dania_dnia)

        self.menu.usun_danie_dnia("Schabowy")

        # Używamy assertLess zamiast assertEqual
        self.assertLess(len(self.menu.dania_dnia), liczba_dan_dnia_przed)
        self.assertNotIn(self.danie1, self.menu.dania_dnia)
        self.assertIn(self.danie2, self.menu.dania_dnia)

    def test_usun_danie_dnia_non_existing(self):
        """Test usunięcia nieistniejącego dania dnia."""
        # Najpierw dodajemy jedno danie dnia
        self.menu.dodaj_danie_dnia("Schabowy")

        # Następnie próbujemy usunąć danie, które nie jest daniem dnia
        with self.assertRaisesRegex(ValueError,
                                    r"Danie .* nie jest na liście dań dnia"):
            self.menu.usun_danie_dnia("Tiramisu")


class TestMenuFindMethods(unittest.TestCase):
    """
    Testy metod wyszukiwania w menu.
    """

    def setUp(self):
        """Przygotowanie danych do testów."""
        self.menu = Menu()

        # Dania główne
        self.schabowy = Danie("Schabowy", 25.99, "danie główne")
        self.gulasz = Danie("Gulasz", 28.50, "danie główne")

        # Zupy
        self.pomidorowa = Danie("Pomidorowa", 12.50, "zupa")

        # Dodawanie dań do menu
        self.menu.dodaj_danie(self.schabowy)
        self.menu.dodaj_danie(self.gulasz)
        self.menu.dodaj_danie(self.pomidorowa)

        # Ustawienie niedostępności niektórych dań
        self.gulasz.ustaw_dostepnosc(False)

    def test_znajdz_dania_po_kategorii_existing(self):
        """Test wyszukiwania dań po istniejącej kategorii."""
        dania = self.menu.znajdz_dania_po_kategorii("danie główne")
        # Używamy assertEqual dla dokładnego porównania długości
        self.assertEqual(len(dania), 2)
        # Używamy assertCountEqual do porównania zawartości list
        # bez względu na kolejność
        self.assertCountEqual(dania, [self.schabowy, self.gulasz])
        self.assertIn(self.schabowy, dania)
        self.assertIn(self.gulasz, dania)

    def test_znajdz_dania_po_kategorii_non_existing(self):
        """Test wyszukiwania dań po nieistniejącej kategorii."""
        dania = self.menu.znajdz_dania_po_kategorii("przystawka")
        # Sprawdzamy, czy wynik to pusta lista
        self.assertEqual(dania, [])
        # Używamy assertFalse zamiast assertEqual
        self.assertFalse(dania)

    def test_znajdz_dania_w_cenie_valid(self):
        """Test wyszukiwania dań w zakresie cenowym."""
        dania = self.menu.znajdz_dania_w_cenie(10.00, 20.00)
        self.assertEqual(len(dania), 1)
        self.assertIn(self.pomidorowa, dania)
        # Sprawdzamy, czy każde znalezione danie ma cenę w podanym zakresie
        for danie in dania:
            self.assertGreaterEqual(danie.cena, 10.00)
            self.assertLessEqual(danie.cena, 20.00)

    def test_znajdz_dania_w_cenie_invalid_range(self):
        """Test wyszukiwania dań w nieprawidłowym zakresie cenowym."""
        with self.assertRaisesRegex(ValueError,
                                    r"Minimalna cena nie może być "
                                    r"większa od maksymalnej"):
            self.menu.znajdz_dania_w_cenie(30.00, 20.00)

    def test_znajdz_dania_w_cenie_excludes_unavailable(self):
        """Test, czy wyszukiwanie dań w zakresie cenowym
         wyklucza niedostępne dania."""
        dania = self.menu.znajdz_dania_w_cenie(25.00, 30.00)
        # Tylko schabowy, gulasz jest niedostępny
        self.assertEqual(len(dania), 1)
        self.assertIn(self.schabowy, dania)
        self.assertNotIn(self.gulasz, dania)

        # Dodatkowo sprawdzamy, czy wszystkie znalezione dania są dostępne
        for danie in dania:
            self.assertTrue(danie.dostepne)

    def test_znajdz_dania_w_cenie_with_partial_range(self):
        """Test wyszukiwania dań, gdy tylko
        część zakresu cenowego zawiera dania."""
        # Zakres 10-30, pokrywa wszystkie dania (12.50, 25.99, 28.50)
        dania = self.menu.znajdz_dania_w_cenie(10.00, 30.00)
        # Tylko dostępne dania: pomidorowa i schabowy
        self.assertEqual(len(dania), 2)

        # Używamy assertCountEqual do sprawdzenia zawartości listy
        # bez względu na kolejność
        self.assertCountEqual(dania, [self.schabowy, self.pomidorowa])

        # Używamy assertRegex do sprawdzenia
        # czy nazwy dań mają odpowiedni format
        for danie in dania:
            self.assertRegex(danie.nazwa, r'^[A-Z][a-z]+$')


if __name__ == '__main__':
    unittest.main()
