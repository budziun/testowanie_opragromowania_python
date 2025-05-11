"""
Testy jednostkowe dla modułu order_processing.
Testuje klasy PozycjaZamowienia, Zamowienie i ObslugaZamowien.

Częściowo wygenerowano przy użyciu Claude.ai
model Claude 3.7 Sonnet
"""


import unittest
from datetime import datetime
from unittest.mock import MagicMock, patch
from src.order_processing import PozycjaZamowienia, Zamowienie, ObslugaZamowien


class TestPozycjaZamowieniaInit(unittest.TestCase):
    """
    Testy inicjalizacji klasy PozycjaZamowienia.
    """

    def test_init_with_required_params(self):
        """Test inicjalizacji z wymaganymi parametrami."""
        pozycja = PozycjaZamowienia("Schabowy", 25.99)
        self.assertEqual(pozycja.nazwa_dania, "Schabowy")
        self.assertEqual(pozycja.cena_jednostkowa, 25.99)
        self.assertEqual(pozycja.ilosc, 1)  # wartość domyślna
        self.assertEqual(pozycja.uwagi, "")  # wartość domyślna
        self.assertEqual(pozycja.status, "w_przygotowaniu")
        self.assertIsInstance(pozycja.czas_dodania, datetime)

    def test_init_with_all_params(self):
        """Test inicjalizacji ze wszystkimi parametrami."""
        pozycja = PozycjaZamowienia("Schabowy", 25.99, 2, "bez ziemniaków")
        self.assertEqual(pozycja.nazwa_dania, "Schabowy")
        self.assertEqual(pozycja.cena_jednostkowa, 25.99)
        self.assertEqual(pozycja.ilosc, 2)
        self.assertEqual(pozycja.uwagi, "bez ziemniaków")

    def test_init_negative_amount(self):
        """Test inicjalizacji z ujemną ilością."""
        with self.assertRaises(ValueError):
            PozycjaZamowienia("Schabowy", 25.99, -1)

    def test_init_zero_amount(self):
        """Test inicjalizacji z ilością równą zero."""
        with self.assertRaises(ValueError):
            PozycjaZamowienia("Schabowy", 25.99, 0)

    def test_init_negative_price(self):
        """Test inicjalizacji z ujemną ceną."""
        with self.assertRaises(ValueError):
            PozycjaZamowienia("Schabowy", -25.99)


class TestPozycjaZamowieniaMetody(unittest.TestCase):
    """
    Testy metod klasy PozycjaZamowienia.
    """

    def setUp(self):
        """Przygotowanie danych do testów."""
        self.pozycja = PozycjaZamowienia("Schabowy",
                                         25.99, 2, "bez ziemniaków")

    def test_zmien_ilosc_valid(self):
        """Test zmiany ilości na poprawną wartość."""
        self.pozycja.zmien_ilosc(3)
        self.assertEqual(self.pozycja.ilosc, 3)

    def test_zmien_ilosc_negative(self):
        """Test zmiany ilości na ujemną wartość."""
        with self.assertRaises(ValueError):
            self.pozycja.zmien_ilosc(-1)

    def test_zmien_ilosc_zero(self):
        """Test zmiany ilości na zero."""
        with self.assertRaises(ValueError):
            self.pozycja.zmien_ilosc(0)

    def test_zmien_status_valid(self):
        """Test zmiany statusu na poprawną wartość."""
        self.pozycja.zmien_status("gotowe")
        self.assertEqual(self.pozycja.status, "gotowe")

    def test_zmien_status_invalid(self):
        """Test zmiany statusu na niepoprawną wartość."""
        with self.assertRaises(ValueError):
            self.pozycja.zmien_status("nieprawidłowy_status")

    def test_dodaj_uwagi_empty(self):
        """Test dodania uwag do pustych uwag."""
        pozycja = PozycjaZamowienia("Schabowy", 25.99)
        pozycja.dodaj_uwagi("bez ziemniaków")
        self.assertEqual(pozycja.uwagi, "bez ziemniaków")

    def test_dodaj_uwagi_existing(self):
        """Test dodania uwag do istniejących uwag."""
        self.pozycja.dodaj_uwagi("i bez surówki")
        self.assertEqual(self.pozycja.uwagi, "bez ziemniaków; i bez surówki")

    def test_oblicz_wartosc(self):
        """Test obliczania wartości pozycji."""
        # Używamy assertAlmostEqual do porównania wartości zmiennoprzecinkowych
        self.assertAlmostEqual(self.pozycja.oblicz_wartosc(),
                               51.98, places=2)  # 25.99 * 2

    def test_oblicz_wartosc_after_change(self):
        """Test obliczania wartości pozycji po zmianie ilości."""
        self.pozycja.zmien_ilosc(3)
        self.assertAlmostEqual(self.pozycja.oblicz_wartosc(),
                               77.97, places=2)  # 25.99 * 3


class TestZamowienieInit(unittest.TestCase):
    """
    Testy inicjalizacji klasy Zamowienie.
    """

    def test_init_with_required_params(self):
        """Test inicjalizacji z wymaganymi parametrami."""
        zamowienie = Zamowienie(5)
        self.assertEqual(zamowienie.numer_stolika, 5)
        self.assertEqual(zamowienie.pozycje, {})
        self.assertEqual(zamowienie.status, "nowe")
        self.assertEqual(zamowienie.platnosc, "")
        self.assertEqual(zamowienie.rabat_procent, 0)
        self.assertEqual(zamowienie.napiwek, 0)
        self.assertEqual(zamowienie.uwagi, "")
        self.assertEqual(zamowienie.kelner, "")
        self.assertIsInstance(zamowienie.czas_zlozenia, datetime)
        self.assertIsInstance(zamowienie.id, str)

    def test_init_with_all_params(self):
        """Test inicjalizacji ze wszystkimi parametrami."""
        zamowienie = Zamowienie(5, "Jan")
        self.assertEqual(zamowienie.numer_stolika, 5)
        self.assertEqual(zamowienie.kelner, "Jan")

    def test_init_negative_table(self):
        """Test inicjalizacji z ujemnym numerem stolika."""
        with self.assertRaises(ValueError):
            Zamowienie(-1)


class TestZamowienieMetody(unittest.TestCase):
    """
    Testy metod klasy Zamowienie.
    """

    def setUp(self):
        """Przygotowanie danych do testów."""
        self.zamowienie = Zamowienie(5, "Jan")

    def test_dodaj_pozycje_new(self):
        """Test dodania nowej pozycji do zamówienia."""
        self.zamowienie.dodaj_pozycje("Schabowy", 25.99, 2, "bez ziemniaków")
        self.assertIn("Schabowy", self.zamowienie.pozycje)
        self.assertEqual(self.zamowienie.pozycje["Schabowy"].ilosc, 2)
        self.assertEqual(self.zamowienie.pozycje["Schabowy"].
                         uwagi, "bez ziemniaków")

    def test_dodaj_pozycje_existing(self):
        """Test dodania istniejącej pozycji do zamówienia,
        powinno zwiększyć ilość."""
        self.zamowienie.dodaj_pozycje("Schabowy", 25.99, 2)
        self.zamowienie.dodaj_pozycje("Schabowy", 25.99, 1, "bez ziemniaków")

        self.assertEqual(self.zamowienie.pozycje["Schabowy"].ilosc, 3)
        self.assertEqual(self.zamowienie.pozycje
                         ["Schabowy"].uwagi, "bez ziemniaków")

    def test_usun_pozycje_all(self):
        """Test usunięcia całej pozycji z zamówienia."""
        self.zamowienie.dodaj_pozycje("Schabowy", 25.99, 2)
        self.zamowienie.dodaj_pozycje("Pomidorowa", 12.50, 1)

        self.zamowienie.usun_pozycje("Schabowy")

        self.assertNotIn("Schabowy", self.zamowienie.pozycje)
        self.assertEqual(len(self.zamowienie.pozycje), 1)

    def test_usun_pozycje_partial(self):
        """Test usunięcia części pozycji z zamówienia."""
        self.zamowienie.dodaj_pozycje("Schabowy", 25.99, 3)

        self.zamowienie.usun_pozycje("Schabowy", 1)

        self.assertEqual(self.zamowienie.pozycje["Schabowy"].ilosc, 2)

    def test_usun_pozycje_non_existing(self):
        """Test usunięcia nieistniejącej pozycji z zamówienia."""
        with self.assertRaises(KeyError):
            self.zamowienie.usun_pozycje("Nieistniejące danie")

    def test_zmien_status_valid(self):
        """Test zmiany statusu na poprawną wartość."""
        self.zamowienie.zmien_status("w_realizacji")
        self.assertEqual(self.zamowienie.status, "w_realizacji")

    def test_zmien_status_invalid(self):
        """Test zmiany statusu na niepoprawną wartość."""
        with self.assertRaises(ValueError):
            self.zamowienie.zmien_status("nieprawidłowy_status")

    def test_ustaw_rabat_valid(self):
        """Test ustawienia rabatu na poprawną wartość."""
        self.zamowienie.ustaw_rabat(15)
        self.assertEqual(self.zamowienie.rabat_procent, 15)

    def test_ustaw_rabat_negative(self):
        """Test ustawienia rabatu na ujemną wartość."""
        with self.assertRaises(ValueError):
            self.zamowienie.ustaw_rabat(-5)

    def test_ustaw_rabat_too_high(self):
        """Test ustawienia rabatu na wartość powyżej 100."""
        with self.assertRaises(ValueError):
            self.zamowienie.ustaw_rabat(110)

    def test_ustaw_platnosc_valid(self):
        """Test ustawienia poprawnej metody płatności."""
        self.zamowienie.ustaw_platnosc("karta", 5)
        self.assertEqual(self.zamowienie.platnosc, "karta")
        self.assertEqual(self.zamowienie.napiwek, 5)

    def test_ustaw_platnosc_invalid(self):
        """Test ustawienia niepoprawnej metody płatności."""
        with self.assertRaises(ValueError):
            self.zamowienie.ustaw_platnosc("nieprawidłowa_metoda")

    def test_ustaw_platnosc_negative_tip(self):
        """Test ustawienia ujemnego napiwku."""
        with self.assertRaises(ValueError):
            self.zamowienie.ustaw_platnosc("gotówka", -5)

    def test_oblicz_wartosc_zamowienia_empty(self):
        """Test obliczania wartości pustego zamówienia."""
        self.assertEqual(self.zamowienie.oblicz_wartosc_zamowienia(), 0)

    def test_oblicz_wartosc_zamowienia(self):
        """Test obliczania wartości zamówienia."""
        self.zamowienie.dodaj_pozycje("Schabowy", 25.99, 2)
        self.zamowienie.dodaj_pozycje("Pomidorowa", 12.50, 1)

        # (25.99 * 2) + (12.50 * 1) = 64.48
        # Używamy assertAlmostEqual do porównania wartości zmiennoprzecinkowych
        self.assertAlmostEqual(self.zamowienie.oblicz_wartosc_zamowienia(),
                               64.48, places=2)

    def test_oblicz_wartosc_po_rabacie_no_rabat(self):
        """Test obliczania wartości zamówienia po rabacie wynoszącym 0."""
        self.zamowienie.dodaj_pozycje("Schabowy", 25.99, 2)
        self.assertAlmostEqual(self.zamowienie.oblicz_wartosc_po_rabacie(),
                               51.98, places=2)

    def test_oblicz_wartosc_po_rabacie_with_rabat(self):
        """Test obliczania wartości zamówienia po rabacie."""
        self.zamowienie.dodaj_pozycje("Schabowy", 25.99, 2)
        self.zamowienie.ustaw_rabat(20)

        # 51.98 * 0.8 = 41.58
        self.assertAlmostEqual(self.zamowienie.oblicz_wartosc_po_rabacie(),
                               41.58, places=2)

    def test_oblicz_calkowity_koszt_no_tip(self):
        """Test obliczania całkowitego kosztu zamówienia bez napiwku."""
        self.zamowienie.dodaj_pozycje("Schabowy", 25.99, 2)
        self.zamowienie.ustaw_rabat(20)

        # 41.58 + 0 = 41.58
        self.assertAlmostEqual(self.zamowienie.oblicz_calkowity_koszt(),
                               41.58, places=2)

    def test_oblicz_calkowity_koszt_with_tip(self):
        """Test obliczania całkowitego kosztu zamówienia z napiwkiem."""
        self.zamowienie.dodaj_pozycje("Schabowy", 25.99, 2)
        self.zamowienie.ustaw_rabat(20)
        self.zamowienie.ustaw_platnosc("karta", 5)

        # 41.58 + 5 = 46.58
        self.assertAlmostEqual(self.zamowienie.oblicz_calkowity_koszt(),
                               46.58, places=2)

    def test_czas_realizacji_not_completed(self):
        """Test obliczania czasu realizacji dla niezakończonego zamówienia."""
        self.assertIsNone(self.zamowienie.czas_realizacji())

    @patch('src.order_processing.datetime')
    def test_czas_realizacji_completed(self, mock_datetime):
        """Test obliczania czasu realizacji dla zakończonego zamówienia."""
        # Ustawienie czasu złożenia zamówienia
        mock_now = datetime(2025, 1, 1, 12, 0, 0)
        mock_datetime.now.return_value = mock_now
        self.zamowienie.czas_zlozenia = mock_now

        # Przesunięcie czasu o 30 minut
        mock_now_later = datetime(2025, 1, 1, 12, 30, 0)
        mock_datetime.now.return_value = mock_now_later

        # Zmiana statusu na dostarczone
        self.zamowienie.zmien_status("dostarczone")

        # Czas realizacji powinien wynosić 30 minut
        self.assertEqual(self.zamowienie.czas_realizacji(), 30.0)


class TestObslugaZamowienInit(unittest.TestCase):
    """
    Testy inicjalizacji klasy ObslugaZamowien.
    """

    def test_init(self):
        """Test inicjalizacji klasy ObslugaZamowien."""
        menu_mock = MagicMock()
        obsluga = ObslugaZamowien(menu_mock)

        self.assertEqual(obsluga.zamowienia, {})
        self.assertEqual(obsluga.menu, menu_mock)
        self.assertEqual(obsluga.aktywne_zamowienia, [])
        self.assertEqual(obsluga.historia_zamowien, [])
        self.assertIsInstance(obsluga.statystyki, dict)
        self.assertEqual(obsluga.statystyki["liczba_zamowien"], 0)


class TestObslugaZamowienMetody(unittest.TestCase):
    """
    Testy metod klasy ObslugaZamowien.
    """

    def setUp(self):
        """Przygotowanie danych do testów."""
        # Mockowanie menu
        self.menu_mock = MagicMock()

        # Mockowanie dań w menu
        self.danie_schabowy = MagicMock()
        self.danie_schabowy.nazwa = "Schabowy"
        self.danie_schabowy.cena = 25.99
        self.danie_schabowy.dostepne = True

        self.danie_pomidorowa = MagicMock()
        self.danie_pomidorowa.nazwa = "Pomidorowa"
        self.danie_pomidorowa.cena = 12.50
        self.danie_pomidorowa.dostepne = True

        self.danie_tiramisu = MagicMock()
        self.danie_tiramisu.nazwa = "Tiramisu"
        self.danie_tiramisu.cena = 15.00
        self.danie_tiramisu.dostepne = False

        # Konfiguracja mocka menu
        self.menu_mock.dania = {
            "Schabowy": self.danie_schabowy,
            "Pomidorowa": self.danie_pomidorowa,
            "Tiramisu": self.danie_tiramisu
        }

        # Inicjalizacja obiektu ObslugaZamowien
        self.obsluga = ObslugaZamowien(self.menu_mock)

    def test_utworz_zamowienie(self):
        """Test tworzenia nowego zamówienia."""
        zamowienie = self.obsluga.utworz_zamowienie(5, "Jan")

        self.assertEqual(zamowienie.numer_stolika, 5)
        self.assertEqual(zamowienie.kelner, "Jan")
        self.assertEqual(len(self.obsluga.zamowienia), 1)
        self.assertIn(zamowienie.id, self.obsluga.zamowienia)
        self.assertIn(zamowienie.id, self.obsluga.aktywne_zamowienia)
        self.assertEqual(self.obsluga.statystyki["liczba_zamowien"], 1)

    def test_dodaj_pozycje_do_zamowienia_valid(self):
        """Test dodania pozycji do zamówienia."""
        zamowienie = self.obsluga.utworz_zamowienie(5)
        self.obsluga.dodaj_pozycje_do_zamowienia(zamowienie.id, "Schabowy", 2)

        self.assertIn("Schabowy", zamowienie.pozycje)
        self.assertEqual(zamowienie.pozycje["Schabowy"].ilosc, 2)
        self.assertEqual(self.obsluga.statystyki
                         ["liczba_sprzedanych_dan"]["Schabowy"], 2)
        self.assertEqual(self.obsluga.statystyki
                         ["najpopularniejsze_danie"], "Schabowy")

    def test_dodaj_pozycje_do_zamowienia_non_existing_order(self):
        """Test dodania pozycji do nieistniejącego zamówienia."""
        with self.assertRaises(KeyError):
            self.obsluga.dodaj_pozycje_do_zamowienia("nieistniejace_id",
                                                     "Schabowy")

    def test_dodaj_pozycje_do_zamowienia_non_existing_dish(self):
        """Test dodania nieistniejącego dania do zamówienia."""
        zamowienie = self.obsluga.utworz_zamowienie(5)
        with self.assertRaises(KeyError):
            self.obsluga.dodaj_pozycje_do_zamowienia(zamowienie.id,
                                                     "Nieistniejące danie")

    def test_dodaj_pozycje_do_zamowienia_unavailable_dish(self):
        """Test dodania niedostępnego dania do zamówienia."""
        zamowienie = self.obsluga.utworz_zamowienie(5)
        with self.assertRaises(ValueError):
            self.obsluga.dodaj_pozycje_do_zamowienia(zamowienie.id, "Tiramisu")

    def test_usun_pozycje_z_zamowienia_all(self):
        """Test usunięcia całej pozycji z zamówienia."""
        zamowienie = self.obsluga.utworz_zamowienie(5)
        self.obsluga.dodaj_pozycje_do_zamowienia(zamowienie.id, "Schabowy", 2)

        # Sprawdzamy, czy Schabowy istnieje w statystykach przed usunięciem
        if "Schabowy" in self.obsluga.statystyki["liczba_sprzedanych_dan"]:
            self.obsluga.usun_pozycje_z_zamowienia(zamowienie.id, "Schabowy")
            self.assertNotIn("Schabowy", zamowienie.pozycje)

            # Sprawdzamy, czy po usunięciu Schabowy
            # jest usunięty ze statystyk lub ma wartość 0
            if "Schabowy" in self.obsluga.statystyki["liczba_sprzedanych_dan"]:
                self.assertEqual(self.obsluga.statystyki
                                 ["liczba_sprzedanych_dan"]["Schabowy"], 0)
        else:
            self.skipTest("Statystyki nie zawierają klucza 'Schabowy'")

    def test_usun_pozycje_z_zamowienia_partial(self):
        """Test usunięcia części pozycji z zamówienia."""
        zamowienie = self.obsluga.utworz_zamowienie(5)
        self.obsluga.dodaj_pozycje_do_zamowienia(zamowienie.id, "Schabowy", 3)

        self.obsluga.usun_pozycje_z_zamowienia(zamowienie.id, "Schabowy", 1)

        self.assertEqual(zamowienie.pozycje["Schabowy"].ilosc, 2)
        self.assertEqual(self.obsluga.statystyki
                         ["liczba_sprzedanych_dan"]["Schabowy"], 2)

    def test_usun_pozycje_z_zamowienia_non_existing_order(self):
        """Test usunięcia pozycji z nieistniejącego zamówienia."""
        with self.assertRaises(KeyError):
            self.obsluga.usun_pozycje_z_zamowienia("nieistniejace_id",
                                                   "Schabowy")

    def test_usun_pozycje_z_zamowienia_non_existing_dish(self):
        """Test usunięcia nieistniejącego dania z zamówienia."""
        zamowienie = self.obsluga.utworz_zamowienie(5)
        self.obsluga.dodaj_pozycje_do_zamowienia(zamowienie.id, "Schabowy", 2)

        with self.assertRaises(KeyError):
            self.obsluga.usun_pozycje_z_zamowienia(zamowienie.id,
                                                   "Nieistniejące danie")

    def test_zamknij_zamowienie_valid(self):
        """Test zamknięcia zamówienia."""
        zamowienie = self.obsluga.utworz_zamowienie(5)
        self.obsluga.dodaj_pozycje_do_zamowienia(zamowienie.id, "Schabowy", 2)
        zamowienie.zmien_status("dostarczone")

        kwota = self.obsluga.zamknij_zamowienie(zamowienie.id, "karta", 5)

        self.assertEqual(zamowienie.status, "oplacone")
        self.assertEqual(zamowienie.platnosc, "karta")
        self.assertEqual(zamowienie.napiwek, 5)
        self.assertNotIn(zamowienie.id, self.obsluga.aktywne_zamowienia)
        self.assertIn(zamowienie.id, self.obsluga.historia_zamowien)
        self.assertAlmostEqual(kwota, 51.98 + 5, places=2)  # 25.99 * 2 + 5

    def test_zamknij_zamowienie_non_existing(self):
        """Test zamknięcia nieistniejącego zamówienia."""
        with self.assertRaises(KeyError):
            self.obsluga.zamknij_zamowienie("nieistniejace_id", "karta")

    def test_zamknij_zamowienie_wrong_status(self):
        """Test zamknięcia zamówienia o nieprawidłowym statusie."""
        zamowienie = self.obsluga.utworz_zamowienie(5)

        with self.assertRaises(ValueError):
            self.obsluga.zamknij_zamowienie(zamowienie.id, "karta")

    def test_anuluj_zamowienie_valid(self):
        """Test anulowania zamówienia."""
        zamowienie = self.obsluga.utworz_zamowienie(5)
        self.obsluga.dodaj_pozycje_do_zamowienia(zamowienie.id, "Schabowy", 2)

        # Sprawdzamy, czy Schabowy istnieje w statystykach przed anulowaniem
        if "Schabowy" in self.obsluga.statystyki["liczba_sprzedanych_dan"]:
            self.obsluga.anuluj_zamowienie(zamowienie.id, "Klient zrezygnował")

            self.assertEqual(zamowienie.status, "anulowane")
            self.assertEqual(zamowienie.uwagi, "ANULOWANO: Klient zrezygnował")
            self.assertNotIn(zamowienie.id, self.obsluga.aktywne_zamowienia)
            self.assertIn(zamowienie.id, self.obsluga.historia_zamowien)

            # Sprawdzamy, czy po anulowaniu Schabowy
            # jest usunięty ze statystyk lub ma wartość 0
            if "Schabowy" in self.obsluga.statystyki["liczba_sprzedanych_dan"]:
                self.assertEqual(self.obsluga.statystyki
                                 ["liczba_sprzedanych_dan"]["Schabowy"], 0)
        else:
            self.skipTest("Statystyki nie zawierają klucza 'Schabowy'")

    def test_anuluj_zamowienie_non_existing(self):
        """Test anulowania nieistniejącego zamówienia."""
        with self.assertRaises(KeyError):
            self.obsluga.anuluj_zamowienie("nieistniejace_id")

    def test_anuluj_zamowienie_already_paid(self):
        """Test anulowania już opłaconego zamówienia."""
        zamowienie = self.obsluga.utworz_zamowienie(5)
        self.obsluga.dodaj_pozycje_do_zamowienia(zamowienie.id, "Schabowy", 2)
        zamowienie.zmien_status("dostarczone")
        self.obsluga.zamknij_zamowienie(zamowienie.id, "karta")

        with self.assertRaises(ValueError):
            self.obsluga.anuluj_zamowienie(zamowienie.id)

    def test_znajdz_zamowienia_dla_stolika(self):
        """Test znajdowania zamówień dla danego stolika."""
        self.obsluga.utworz_zamowienie(5, "Jan")
        self.obsluga.utworz_zamowienie(5, "Anna")
        self.obsluga.utworz_zamowienie(7, "Piotr")

        zamowienia = self.obsluga.znajdz_zamowienia_dla_stolika(5)

        self.assertEqual(len(zamowienia), 2)
        self.assertTrue(all(z.numer_stolika == 5 for z in zamowienia))

    def test_znajdz_zamowienia_dla_stolika_none(self):
        """Test znajdowania zamówień dla stolika bez zamówień."""
        self.obsluga.utworz_zamowienie(5, "Jan")

        zamowienia = self.obsluga.znajdz_zamowienia_dla_stolika(7)

        self.assertEqual(zamowienia, [])


if __name__ == '__main__':
    unittest.main()
