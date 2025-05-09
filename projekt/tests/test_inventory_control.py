"""
Testy jednostkowe dla modułu inventory_control.
Testuje klasy Skladnik i ZarzadzanieSkladnikami.
"""

import unittest
from datetime import datetime, timedelta
from src.inventory_control import Skladnik, ZarzadzanieSkladnikami


class TestSkladnikInit(unittest.TestCase):
    """
    Testy inicjalizacji klasy Skladnik.
    """

    def test_init_with_required_params(self):
        """Test inicjalizacji z wymaganymi parametrami."""
        skladnik = Skladnik("Mąka", "kg")
        self.assertEqual(skladnik.nazwa, "Mąka")
        self.assertEqual(skladnik.jednostka, "kg")
        self.assertEqual(skladnik.ilosc_na_stanie, 0)  # wartość domyślna
        self.assertEqual(skladnik.min_ilosc, 10)  # wartość domyślna
        self.assertEqual(skladnik.cena_jednostkowa, 0)  # wartość domyślna
        self.assertIsNone(skladnik.data_waznosci)  # wartość domyślna
        self.assertEqual(skladnik.dostawca, "")  # wartość domyślna
        self.assertEqual(skladnik.kategoria, "")  # wartość domyślna
        self.assertEqual(skladnik.lokalizacja, "")  # wartość domyślna

    def test_init_with_all_params(self):
        """Test inicjalizacji ze wszystkimi parametrami."""
        data_waznosci = datetime.now() + timedelta(days=30)
        skladnik = Skladnik(
            "Mąka", "kg", 5, 2, 3.50,
            data_waznosci, "Firma X", "Suche", "Półka A"
        )
        self.assertEqual(skladnik.nazwa, "Mąka")
        self.assertEqual(skladnik.jednostka, "kg")
        self.assertEqual(skladnik.ilosc_na_stanie, 5)
        self.assertEqual(skladnik.min_ilosc, 2)
        self.assertEqual(skladnik.cena_jednostkowa, 3.50)
        self.assertEqual(skladnik.data_waznosci, data_waznosci)
        self.assertEqual(skladnik.dostawca, "Firma X")
        self.assertEqual(skladnik.kategoria, "Suche")
        self.assertEqual(skladnik.lokalizacja, "Półka A")

    def test_init_negative_amount(self):
        """Test inicjalizacji z ujemną ilością."""
        with self.assertRaises(ValueError):
            Skladnik("Mąka", "kg", -5)

    def test_init_negative_min_amount(self):
        """Test inicjalizacji z ujemną minimalną ilością."""
        with self.assertRaises(ValueError):
            Skladnik("Mąka", "kg", 5, -2)

    def test_init_negative_price(self):
        """Test inicjalizacji z ujemną ceną."""
        with self.assertRaises(ValueError):
            Skladnik("Mąka", "kg", 5, 2, -3.50)

    def test_historia_zmian_initial(self):
        """Test inicjalizacji historii zmian."""
        skladnik = Skladnik("Mąka", "kg", 5)
        self.assertEqual(len(skladnik.historia_zmian), 1)
        self.assertEqual(skladnik.historia_zmian[0][1], "początkowy stan")
        self.assertEqual(skladnik.historia_zmian[0][2], 5)

    def test_historia_zmian_empty(self):
        """Test inicjalizacji historii zmian dla początkowej ilości zero."""
        skladnik = Skladnik("Mąka", "kg")
        self.assertEqual(len(skladnik.historia_zmian), 0)


class TestSkladnikMetody(unittest.TestCase):
    """
    Testy metod klasy Skladnik.
    """

    def setUp(self):
        """Przygotowanie danych do testów."""
        self.skladnik = Skladnik("Mąka", "kg", 5, 2, 3.50)

    def test_dodaj_zapas(self):
        """Test dodawania zapasu."""
        self.skladnik.dodaj_zapas(3)
        self.assertEqual(self.skladnik.ilosc_na_stanie, 8)
        self.assertEqual(len(self.skladnik.historia_zmian), 2)
        self.assertEqual(self.skladnik.historia_zmian[1][1], "dostawa")
        self.assertEqual(self.skladnik.historia_zmian[1][2], 3)

    def test_dodaj_zapas_with_id(self):
        """Test dodawania zapasu z identyfikatorem dostawy."""
        self.skladnik.dodaj_zapas(3, "1234")
        self.assertEqual(self.skladnik.ilosc_na_stanie, 8)
        self.assertEqual(len(self.skladnik.historia_zmian), 2)
        self.assertEqual(self.skladnik.historia_zmian[1][1], "dostawa 1234")
        self.assertEqual(self.skladnik.historia_zmian[1][2], 3)

    def test_dodaj_zapas_negative(self):
        """Test dodawania ujemnego zapasu."""
        with self.assertRaises(ValueError):
            self.skladnik.dodaj_zapas(-3)

    def test_dodaj_zapas_zero(self):
        """Test dodawania zerowego zapasu."""
        with self.assertRaises(ValueError):
            self.skladnik.dodaj_zapas(0)

    def test_zuzyj(self):
        """Test zużywania składnika."""
        self.skladnik.zuzyj(2)
        self.assertEqual(self.skladnik.ilosc_na_stanie, 3)
        self.assertEqual(len(self.skladnik.historia_zmian), 2)
        self.assertEqual(self.skladnik.historia_zmian[1][1], "zużycie")
        self.assertEqual(self.skladnik.historia_zmian[1][2], -2)

    def test_zuzyj_with_cel(self):
        """Test zużywania składnika z celem."""
        self.skladnik.zuzyj(2, "Ciasto")
        self.assertEqual(self.skladnik.ilosc_na_stanie, 3)
        self.assertEqual(len(self.skladnik.historia_zmian), 2)
        self.assertEqual(self.skladnik.historia_zmian[1][1], "zużycie Ciasto")
        self.assertEqual(self.skladnik.historia_zmian[1][2], -2)

    def test_zuzyj_negative(self):
        """Test zużywania ujemnej ilości."""
        with self.assertRaises(ValueError):
            self.skladnik.zuzyj(-2)

    def test_zuzyj_zero(self):
        """Test zużywania zerowej ilości."""
        with self.assertRaises(ValueError):
            self.skladnik.zuzyj(0)

    def test_zuzyj_too_much(self):
        """Test zużywania większej ilości niż jest na stanie."""
        with self.assertRaises(ValueError):
            self.skladnik.zuzyj(10)

    def test_zmien_cene(self):
        """Test zmiany ceny."""
        self.skladnik.zmien_cene(4.50)
        self.assertEqual(self.skladnik.cena_jednostkowa, 4.50)

    def test_zmien_cene_negative(self):
        """Test zmiany ceny na ujemną."""
        with self.assertRaises(ValueError):
            self.skladnik.zmien_cene(-4.50)

    def test_ustaw_date_waznosci(self):
        """Test ustawiania daty ważności."""
        data_waznosci = datetime.now() + timedelta(days=30)
        self.skladnik.ustaw_date_waznosci(data_waznosci)
        self.assertEqual(self.skladnik.data_waznosci, data_waznosci)

    def test_ustaw_date_waznosci_past(self):
        """Test ustawiania daty ważności w przeszłości."""
        data_waznosci = datetime.now() - timedelta(days=1)
        with self.assertRaises(ValueError):
            self.skladnik.ustaw_date_waznosci(data_waznosci)

    def test_czy_wymaga_zamowienia_true(self):
        """Test sprawdzania czy składnik wymaga zamówienia - prawda."""
        self.skladnik.ilosc_na_stanie = 1
        self.assertTrue(self.skladnik.czy_wymaga_zamowienia())

    def test_czy_wymaga_zamowienia_false(self):
        """Test sprawdzania czy składnik wymaga zamówienia - fałsz."""
        self.skladnik.ilosc_na_stanie = 5
        self.assertFalse(self.skladnik.czy_wymaga_zamowienia())

    def test_czy_przeterminowany_true(self):
        """Test sprawdzania czy składnik jest przeterminowany - prawda."""
        # Ustawiamy datę ważności na przeszłość (do testów)
        self.skladnik.data_waznosci = datetime.now() - timedelta(days=1)
        self.assertTrue(self.skladnik.czy_przeterminowany())

    def test_czy_przeterminowany_false(self):
        """Test sprawdzania czy składnik jest przeterminowany - fałsz."""
        self.skladnik.data_waznosci = datetime.now() + timedelta(days=1)
        self.assertFalse(self.skladnik.czy_przeterminowany())

    def test_czy_przeterminowany_none(self):
        """Test sprawdzania czy składnik jest przeterminowany; brak daty"""
        self.assertFalse(self.skladnik.czy_przeterminowany())

    def test_wartosc_zapasu(self):
        """Test obliczania wartości zapasu."""
        # 5 * 3.50
        self.assertAlmostEqual(self.skladnik.wartosc_zapasu(), 17.50)


class TestZarzadzanieSkladnikamiInit(unittest.TestCase):
    """
    Testy inicjalizacji klasy ZarzadzanieSkladnikami.
    """

    def test_init(self):
        """Test inicjalizacji."""
        zarzadzanie = ZarzadzanieSkladnikami()
        self.assertEqual(zarzadzanie.skladniki, {})
        self.assertEqual(zarzadzanie.przepisy, {})
        self.assertEqual(zarzadzanie.dostawy, [])
        self.assertEqual(zarzadzanie.kategorie_skladnikow, set())
        self.assertEqual(zarzadzanie.dostawcy, set())


class TestZarzadzanieSkladnikamiMetody(unittest.TestCase):
    """
    Testy metod klasy ZarzadzanieSkladnikami.
    """

    def setUp(self):
        """Przygotowanie danych do testów."""
        self.zarzadzanie = ZarzadzanieSkladnikami()

        self.maka = Skladnik("Mąka", "kg", 5, 2, 3.50, None,
                             "Dostawca X", "Suche")
        self.cukier = Skladnik("Cukier", "kg", 3, 1, 4.20, None,
                               "Dostawca Y", "Suche")
        self.maslo = Skladnik("Masło", "kg", 2, 0.5, 18.50, None,
                              "Dostawca X", "Nabiał")

        self.przepis_ciasto = {
            "Mąka": 0.5,
            "Cukier": 0.3,
            "Masło": 0.2
        }

    def test_dodaj_skladnik_single(self):
        """Test dodawania pojedynczego składnika."""
        self.zarzadzanie.dodaj_skladnik(self.maka)
        self.assertIn("Mąka", self.zarzadzanie.skladniki)
        # Sprawidzamy, czy kategoria została dodana
        self.assertIn("Suche", self.zarzadzanie.kategorie_skladnikow)
        # Sprawdzamy, czy dostawca został dodany
        self.assertIn("Dostawca X", self.zarzadzanie.dostawcy)

    def test_dodaj_skladnik_duplicate(self):
        """Test dodawania duplikatu składnika."""
        self.zarzadzanie.dodaj_skladnik(self.maka)
        with self.assertRaises(ValueError):
            self.zarzadzanie.dodaj_skladnik(self.maka)

    def test_dodaj_skladnik_multiple(self):
        """Test dodawania wielu składników."""
        self.zarzadzanie.dodaj_skladnik(self.maka)
        self.zarzadzanie.dodaj_skladnik(self.cukier)
        self.assertEqual(len(self.zarzadzanie.skladniki), 2)
        self.assertEqual(len(self.zarzadzanie.kategorie_skladnikow), 1)
        self.assertEqual(len(self.zarzadzanie.dostawcy), 2)

    def test_usun_skladnik(self):
        """Test usuwania składnika."""
        self.zarzadzanie.dodaj_skladnik(self.maka)
        self.zarzadzanie.usun_skladnik("Mąka")
        self.assertNotIn("Mąka", self.zarzadzanie.skladniki)
        self.assertNotIn("Suche", self.zarzadzanie.kategorie_skladnikow)
        self.assertNotIn("Dostawca X", self.zarzadzanie.dostawcy)

    def test_usun_skladnik_non_existing(self):
        """Test usuwania nieistniejącego składnika."""
        with self.assertRaises(KeyError):
            self.zarzadzanie.usun_skladnik("Nieistniejący")

    def test_usun_skladnik_used_in_recipe(self):
        """Test usuwania składnika używanego w przepisie."""
        self.zarzadzanie.dodaj_skladnik(self.maka)
        self.zarzadzanie.dodaj_skladnik(self.cukier)
        self.zarzadzanie.dodaj_skladnik(self.maslo)
        self.zarzadzanie.dodaj_przepis("Ciasto", self.przepis_ciasto)

        with self.assertRaises(ValueError):
            self.zarzadzanie.usun_skladnik("Mąka")

    def test_usun_skladnik_not_last_in_category(self):
        """Test usuwania składnika, który nie jest
        ostatnim składnikiem w swojej kategorii."""
        self.zarzadzanie.dodaj_skladnik(self.maka)
        self.zarzadzanie.dodaj_skladnik(self.cukier)
        self.zarzadzanie.dodaj_skladnik(self.maslo)

        # Upewniamy się, że wszystkie składniki zostały dodane prawidłowo
        self.assertEqual(len(self.zarzadzanie.skladniki), 3)
        # "Suche" i "Nabiał"
        self.assertEqual(len(self.zarzadzanie.kategorie_skladnikow), 2)
        # "Dostawca X" i "Dostawca Y"
        self.assertEqual(len(self.zarzadzanie.dostawcy), 2)

        # Usuwamy mąkę - kategorię "Suche" wciąż reprezentuje cukier,
        # a "Dostawca X" wciąż dostarcza masło
        self.zarzadzanie.usun_skladnik("Mąka")

        self.assertNotIn("Mąka", self.zarzadzanie.skladniki)
        # Kategoria pozostaje (cukier)
        self.assertIn("Suche", self.zarzadzanie.kategorie_skladnikow)
        # Dostawca pozostaje (masło)
        self.assertIn("Dostawca X", self.zarzadzanie.dostawcy)
        # Dostawca Y również pozostaje (cukier)
        self.assertIn("Dostawca Y", self.zarzadzanie.dostawcy)

        # Usuwamy cukier - teraz kategoria "Suche" znika,
        # ale "Dostawca Y" też znika
        # bo tylko cukier był od tego dostawcy
        self.zarzadzanie.usun_skladnik("Cukier")

        # Już nie ma składników w kategorii "Suche"
        self.assertNotIn("Suche", self.zarzadzanie.kategorie_skladnikow)
        # Dostawca Y już nie ma żadnych produktów
        self.assertNotIn("Dostawca Y", self.zarzadzanie.dostawcy)
        # Dostawca X wciąż dostarcza masło
        self.assertIn("Dostawca X", self.zarzadzanie.dostawcy)
        # Kategoria "Nabiał" pozostaje (masło)
        self.assertIn("Nabiał", self.zarzadzanie.kategorie_skladnikow)

    def test_dodaj_przepis(self):
        """Test dodawania przepisu."""
        self.zarzadzanie.dodaj_skladnik(self.maka)
        self.zarzadzanie.dodaj_skladnik(self.cukier)
        self.zarzadzanie.dodaj_skladnik(self.maslo)

        self.zarzadzanie.dodaj_przepis("Ciasto", self.przepis_ciasto)

        self.assertIn("Ciasto", self.zarzadzanie.przepisy)
        self.assertEqual(self.zarzadzanie.przepisy["Ciasto"],
                         self.przepis_ciasto)

    def test_dodaj_przepis_empty(self):
        """Test dodawania pustego przepisu."""
        with self.assertRaises(ValueError):
            self.zarzadzanie.dodaj_przepis("Pusty przepis", {})

    def test_dodaj_przepis_non_existing_skladnik(self):
        """Test dodawania przepisu z nieistniejącym składnikiem."""
        with self.assertRaises(KeyError):
            self.zarzadzanie.dodaj_przepis("Ciasto", {"Nieistniejący": 1})

    def test_dodaj_przepis_duplicate(self):
        """Test dodawania duplikatu przepisu."""
        self.zarzadzanie.dodaj_skladnik(self.maka)
        self.zarzadzanie.dodaj_skladnik(self.cukier)
        self.zarzadzanie.dodaj_skladnik(self.maslo)

        self.zarzadzanie.dodaj_przepis("Ciasto", self.przepis_ciasto)

        with self.assertRaises(ValueError):
            self.zarzadzanie.dodaj_przepis("Ciasto", {"Mąka": 1})

    def test_aktualizuj_przepis(self):
        """Test aktualizacji przepisu."""
        self.zarzadzanie.dodaj_skladnik(self.maka)
        self.zarzadzanie.dodaj_skladnik(self.cukier)
        self.zarzadzanie.dodaj_skladnik(self.maslo)

        self.zarzadzanie.dodaj_przepis("Ciasto", self.przepis_ciasto)

        nowy_przepis = {"Mąka": 0.6, "Cukier": 0.4}
        self.zarzadzanie.aktualizuj_przepis("Ciasto", nowy_przepis)

        self.assertEqual(self.zarzadzanie.przepisy["Ciasto"], nowy_przepis)

    def test_aktualizuj_przepis_non_existing(self):
        """Test aktualizacji nieistniejącego przepisu."""
        self.zarzadzanie.dodaj_skladnik(self.maka)

        with self.assertRaises(KeyError):
            self.zarzadzanie.aktualizuj_przepis("Nieistniejący", {"Mąka": 1})

    def test_aktualizuj_przepis_empty(self):
        """Test aktualizacji przepisu na pusty."""
        self.zarzadzanie.dodaj_skladnik(self.maka)
        self.zarzadzanie.dodaj_przepis("Ciasto", {"Mąka": 1})

        with self.assertRaises(ValueError):
            self.zarzadzanie.aktualizuj_przepis("Ciasto", {})

    def test_aktualizuj_przepis_non_existing_skladnik(self):
        """Test aktualizacji przepisu z nieistniejącym składnikiem."""
        self.zarzadzanie.dodaj_skladnik(self.maka)
        self.zarzadzanie.dodaj_przepis("Ciasto", {"Mąka": 1})

        with self.assertRaises(KeyError):
            self.zarzadzanie.aktualizuj_przepis("Ciasto", {"Nieistniejący": 1})

    def test_usun_przepis(self):
        """Test usuwania przepisu."""
        self.zarzadzanie.dodaj_skladnik(self.maka)
        self.zarzadzanie.dodaj_przepis("Ciasto", {"Mąka": 1})

        self.zarzadzanie.usun_przepis("Ciasto")

        self.assertNotIn("Ciasto", self.zarzadzanie.przepisy)

    def test_usun_przepis_non_existing(self):
        """Test usuwania nieistniejącego przepisu."""
        with self.assertRaises(KeyError):
            self.zarzadzanie.usun_przepis("Nieistniejący")

    def test_sprawdz_mozliwosc_przygotowania_true(self):
        """Test sprawdzania możliwości przygotowania - prawda."""
        self.zarzadzanie.dodaj_skladnik(self.maka)
        self.zarzadzanie.dodaj_skladnik(self.cukier)
        self.zarzadzanie.dodaj_skladnik(self.maslo)
        self.zarzadzanie.dodaj_przepis("Ciasto", self.przepis_ciasto)

        self.assertTrue(self.zarzadzanie.sprawdz_mozliwosc_przygotowania
                        ("Ciasto"))

    def test_sprawdz_mozliwosc_przygotowania_false(self):
        """Test sprawdzania możliwości przygotowania - fałsz."""
        self.zarzadzanie.dodaj_skladnik(self.maka)
        self.zarzadzanie.dodaj_skladnik(self.cukier)
        self.zarzadzanie.dodaj_skladnik(self.maslo)
        self.zarzadzanie.dodaj_przepis("Ciasto", self.przepis_ciasto)

        # Można zrobić maksymalnie 10 porcji (5kg mąki po 0.5kg na porcję)
        self.assertFalse(self.zarzadzanie.sprawdz_mozliwosc_przygotowania
                         ("Ciasto", 11))

    def test_sprawdz_mozliwosc_przygotowania_non_existing(self):
        """Test możliwości przygotowania nieistniejącego przepisu."""
        with self.assertRaises(KeyError):
            self.zarzadzanie.sprawdz_mozliwosc_przygotowania("Nieistniejący")

    def test_przygotuj_danie(self):
        """Test przygotowania dania."""
        self.zarzadzanie.dodaj_skladnik(self.maka)
        self.zarzadzanie.dodaj_skladnik(self.cukier)
        self.zarzadzanie.dodaj_skladnik(self.maslo)
        self.zarzadzanie.dodaj_przepis("Ciasto", self.przepis_ciasto)

        self.zarzadzanie.przygotuj_danie("Ciasto")

        # Sprawdzenie, czy składniki zostały zużyte
        self.assertEqual(self.zarzadzanie.skladniki["Mąka"]
                         .ilosc_na_stanie, 4.5)  # 5 - 0.5
        self.assertEqual(self.zarzadzanie.skladniki["Cukier"]
                         .ilosc_na_stanie, 2.7)  # 3 - 0.3
        self.assertEqual(self.zarzadzanie.skladniki["Masło"]
                         .ilosc_na_stanie, 1.8)  # 2 - 0.2

    def test_przygotuj_danie_multiple(self):
        """Test przygotowania wielu porcji dania."""
        self.zarzadzanie.dodaj_skladnik(self.maka)
        self.zarzadzanie.dodaj_skladnik(self.cukier)
        self.zarzadzanie.dodaj_skladnik(self.maslo)
        self.zarzadzanie.dodaj_przepis("Ciasto", self.przepis_ciasto)

        self.zarzadzanie.przygotuj_danie("Ciasto", 2)

        # Sprawdzenie, czy składniki zostały zużyte
        self.assertEqual(self.zarzadzanie.skladniki["Mąka"]
                         .ilosc_na_stanie, 4)  # 5 - 0.5*2
        self.assertEqual(self.zarzadzanie.skladniki["Cukier"]
                         .ilosc_na_stanie, 2.4)  # 3 - 0.3*2
        self.assertEqual(self.zarzadzanie.skladniki["Masło"]
                         .ilosc_na_stanie, 1.6)  # 2 - 0.2*2

    def test_przygotuj_danie_non_existing(self):
        """Test przygotowania nieistniejącego dania."""
        with self.assertRaises(KeyError):
            self.zarzadzanie.przygotuj_danie("Nieistniejący")

    def test_przygotuj_danie_not_enough(self):
        """Test przygotowania dania,
        gdy nie ma wystarczającej ilości składników."""
        self.zarzadzanie.dodaj_skladnik(self.maka)
        self.zarzadzanie.dodaj_skladnik(self.cukier)
        self.zarzadzanie.dodaj_skladnik(self.maslo)
        self.zarzadzanie.dodaj_przepis("Ciasto", self.przepis_ciasto)

        with self.assertRaises(ValueError):
            self.zarzadzanie.przygotuj_danie("Ciasto", 20)

    def test_zarejestruj_dostawe(self):
        """Test rejestrowania dostawy."""
        self.zarzadzanie.dodaj_skladnik(self.maka)

        # Dostawa: 10kg mąki po 3.00zł/kg
        self.zarzadzanie.zarejestruj_dostawe("Dostawca Z",
                                             {"Mąka": (10, 3.00)})

        self.assertEqual(len(self.zarzadzanie.dostawy), 1)
        self.assertEqual(self.zarzadzanie.skladniki["Mąka"]
                         .ilosc_na_stanie, 15)  # 5 + 10
        self.assertEqual(self.zarzadzanie.skladniki["Mąka"]
                         .cena_jednostkowa, 3.00)
        self.assertIn("Dostawca Z", self.zarzadzanie.dostawcy)

    def test_zarejestruj_dostawe_non_existing_skladnik(self):
        """Test rejestrowania dostawy z nieistniejącym składnikiem."""
        with self.assertRaises(KeyError):
            self.zarzadzanie.zarejestruj_dostawe("Dostawca Z",
                                                 {"Nieistniejący": (10, 3.00)})

    def test_lista_do_zamowienia(self):
        """Test tworzenia listy składników do zamówienia."""
        self.zarzadzanie.dodaj_skladnik(self.maka)
        self.zarzadzanie.dodaj_skladnik(self.cukier)
        self.zarzadzanie.dodaj_skladnik(self.maslo)

        # Używamy składników, aby spadły poniżej minimalnej ilości
        self.maka.zuzyj(4)  # Zostanie 1 (min 2)
        self.cukier.zuzyj(1)  # Zostanie 2 (min 1)
        self.maslo.zuzyj(1.6)  # Zostanie 0.4 (min 0.5)

        lista = self.zarzadzanie.lista_do_zamowienia()

        self.assertEqual(len(lista), 2)  # Mąka i Masło wymagają zamówienia
        self.assertIn(self.maka, lista)
        self.assertIn(self.maslo, lista)

    def test_znajdz_przeterminowane(self):
        """Test znajdowania przeterminowanych składników."""
        self.zarzadzanie.dodaj_skladnik(self.maka)

        przeterminowany = Skladnik("Jogurt", "szt", 5, 2, 1.50)
        przeterminowany.data_waznosci = datetime.now() - timedelta(days=1)
        self.zarzadzanie.dodaj_skladnik(przeterminowany)

        przeterminowane = self.zarzadzanie.znajdz_przeterminowane()

        self.assertEqual(len(przeterminowane), 1)
        self.assertIn(przeterminowany, przeterminowane)

    def test_oblicz_wartosc_magazynu(self):
        """Test obliczania wartości magazynu."""
        self.zarzadzanie.dodaj_skladnik(self.maka)
        self.zarzadzanie.dodaj_skladnik(self.cukier)
        self.zarzadzanie.dodaj_skladnik(self.maslo)

        # 5kg * 3.50 + 3kg * 4.20 + 2kg * 18.50 = 17.50 + 12.60 + 37.00 = 67.10
        self.assertAlmostEqual(self.zarzadzanie.oblicz_wartosc_magazynu(),
                               67.10)


if __name__ == '__main__':
    unittest.main()
