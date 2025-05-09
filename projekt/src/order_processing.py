"""
Moduł obsługujący zamówienia w restauracji.
Zawiera klasy do tworzenia, przetwarzania i rozliczania zamówień.

Kod aplikacji z modułu order_processing.py wygenerwoany przy użyciu Claude.ai
model Claude Sonnet 3.7
"""

from datetime import datetime
from typing import List, Optional, Dict, Any, TypedDict
import uuid


class StatystykiDict(TypedDict):
    """Definicja typu dla słownika statystyk."""
    liczba_zamowien: int
    suma_wartosci: float
    srednia_wartosc: float
    najpopularniejsze_danie: str
    liczba_sprzedanych_dan: Dict[str, int]


class PozycjaZamowienia:
    """
    Klasa reprezentująca pojedynczą pozycję w zamówieniu.

    Atrybuty:
        nazwa_dania (str): Nazwa zamówionego dania.
        ilosc (int): Liczba zamówionych porcji.
        cena_jednostkowa (float): Cena jednej porcji.
        uwagi (str): Dodatkowe uwagi do zamówienia (np. bez cebuli).
        status (str): Status pozycji (w_przygotowaniu, gotowe, podane).
        czas_dodania (datetime): Czas dodania pozycji do zamówienia.
    """

    def __init__(self, nazwa_dania: str, cena_jednostkowa: float,
                 ilosc: int = 1, uwagi: str = ""):
        """
        Inicjalizuje nową pozycję zamówienia.

        Args:
            nazwa_dania: Nazwa zamówionego dania.
            cena_jednostkowa: Cena jednej porcji.
            ilosc: Liczba zamówionych porcji.
            uwagi: Dodatkowe uwagi do zamówienia.

        Raises:
            ValueError: Gdy ilość jest mniejsza od 1 lub cena jest ujemna.
        """
        if ilosc < 1:
            raise ValueError("Ilość musi być większa od zera")
        if cena_jednostkowa < 0:
            raise ValueError("Cena nie może być ujemna")

        self.nazwa_dania = nazwa_dania
        self.ilosc = ilosc
        self.cena_jednostkowa = cena_jednostkowa
        self.uwagi = uwagi
        self.status = "w_przygotowaniu"
        self.czas_dodania = datetime.now()

    def zmien_ilosc(self, nowa_ilosc: int) -> None:
        """
        Zmienia ilość zamówionych porcji.

        Args:
            nowa_ilosc: Nowa liczba porcji.

        Raises:
            ValueError: Gdy nowa ilość jest mniejsza od 1.
        """
        if nowa_ilosc < 1:
            raise ValueError("Ilość musi być większa od zera")
        self.ilosc = nowa_ilosc

    def zmien_status(self, nowy_status: str) -> None:
        """
        Zmienia status pozycji zamówienia.

        Args:
            nowy_status: Nowy status pozycji.

        Raises:
            ValueError: Gdy status jest nieprawidłowy.
        """
        dozwolone_statusy = ["w_przygotowaniu", "gotowe", "podane"]
        if nowy_status not in dozwolone_statusy:
            raise ValueError(f"Nieprawidłowy status: {nowy_status}")
        self.status = nowy_status

    def dodaj_uwagi(self, uwagi: str) -> None:
        """
        Dodaje uwagi do pozycji zamówienia.

        Args:
            uwagi: Uwagi do dodania.
        """
        if self.uwagi:
            self.uwagi += "; " + uwagi
        else:
            self.uwagi = uwagi

    def oblicz_wartosc(self) -> float:
        """
        Oblicza wartość pozycji zamówienia.

        Returns:
            Wartość pozycji (cena * ilość).
        """
        return round(self.cena_jednostkowa * self.ilosc, 2)


class Zamowienie:
    """
    Klasa reprezentująca całe zamówienie.

    Atrybuty:
        id (str): Unikalny identyfikator zamówienia.
        numer_stolika (int): Numer stolika.
        pozycje (Dict[str, PozycjaZamowienia]): Słownik pozycji zamówienia.
        czas_zlozenia (datetime): Czas złożenia zamówienia.
        status (str): Status całego zamówienia.
        platnosc (str): Metoda płatności.
        rabat_procent (float): Procent rabatu na całe zamówienie.
        napiwek (float): Kwota napiwku.
        uwagi (str): Ogólne uwagi do zamówienia.
        kelner (str): Imię kelnera obsługującego zamówienie.
    """

    def __init__(self, numer_stolika: int, kelner: str = ""):
        """
        Inicjalizuje nowe zamówienie.

        Args:
            numer_stolika: Numer stolika.
            kelner: Imię kelnera obsługującego zamówienie.

        Raises:
            ValueError: Gdy numer stolika jest ujemny.
        """
        if numer_stolika < 0:
            raise ValueError("Numer stolika nie może być ujemny")

        self.id = str(uuid.uuid4())
        self.numer_stolika = numer_stolika
        self.pozycje: Dict[str, PozycjaZamowienia] = {}
        self.czas_zlozenia = datetime.now()
        # nowe, w_realizacji, gotowe, dostarczone, anulowane, oplacone
        self.status = "nowe"
        self.platnosc = ""  # gotówka, karta, blik
        self.rabat_procent = 0.0
        self.napiwek = 0.0
        self.uwagi = ""
        self.kelner = kelner

    def dodaj_pozycje(self, nazwa_dania: str, cena_jednostkowa: float,
                      ilosc: int = 1, uwagi: str = "") -> None:
        """
        Dodaje pozycję do zamówienia.

        Args:
            nazwa_dania: Nazwa dania.
            cena_jednostkowa: Cena jednostkowa dania.
            ilosc: Liczba porcji.
            uwagi: Dodatkowe uwagi.

        Raises:
            ValueError: Gdy pozycja już istnieje w zamówieniu.
        """
        if nazwa_dania in self.pozycje:
            nowa_ilosc = self.pozycje[nazwa_dania].ilosc + ilosc
            self.pozycje[nazwa_dania].zmien_ilosc(nowa_ilosc)
            if uwagi:
                self.pozycje[nazwa_dania].dodaj_uwagi(uwagi)
        else:
            self.pozycje[nazwa_dania] = PozycjaZamowienia(
                nazwa_dania, cena_jednostkowa, ilosc, uwagi)

    def usun_pozycje(self, nazwa_dania: str,
                     ilosc: Optional[int] = None) -> None:
        """
        Usuwa pozycję z zamówienia.

        Args:
            nazwa_dania: Nazwa dania do usunięcia.
            ilosc: Liczba porcji do usunięcia (None = wszystkie).

        Raises:
            KeyError: Gdy danie nie znajduje się w zamówieniu.
        """
        if nazwa_dania not in self.pozycje:
            raise KeyError(f"Danie {nazwa_dania} "
                           f"nie znajduje się w zamówieniu")

        if ilosc is None or ilosc >= self.pozycje[nazwa_dania].ilosc:
            del self.pozycje[nazwa_dania]
        else:
            nowa_ilosc = self.pozycje[nazwa_dania].ilosc - ilosc
            self.pozycje[nazwa_dania].zmien_ilosc(nowa_ilosc)

    def zmien_status(self, nowy_status: str) -> None:
        """
        Zmienia status zamówienia.

        Args:
            nowy_status: Nowy status zamówienia.

        Raises:
            ValueError: Gdy status jest nieprawidłowy.
        """
        dozwolone_statusy = ["nowe", "w_realizacji", "gotowe",
                             "dostarczone", "anulowane", "oplacone"]
        if nowy_status not in dozwolone_statusy:
            raise ValueError(f"Niedozwolony status: {nowy_status}")
        self.status = nowy_status

    def ustaw_rabat(self, rabat_procent: float) -> None:
        """
        Ustawia rabat dla całego zamówienia.

        Args:
            rabat_procent: Procent rabatu (0-100).

        Raises:
            ValueError: Gdy rabat jest spoza zakresu 0-100.
        """
        if rabat_procent < 0 or rabat_procent > 100:
            raise ValueError("Rabat musi być wartością między 0 a 100")
        self.rabat_procent = rabat_procent

    def ustaw_platnosc(self, metoda: str, napiwek: float = 0) -> None:
        """
        Ustawia metodę płatności i ewentualny napiwek.

        Args:
            metoda: Metoda płatności.
            napiwek: Kwota napiwku.

        Raises:
            ValueError: Gdy metoda płatności jest nieprawidłowa
             lub napiwek jest ujemny.
        """
        dozwolone_metody = ["gotówka", "karta", "blik"]
        if metoda not in dozwolone_metody:
            raise ValueError(f"Niedozwolona metoda płatności: {metoda}")

        if napiwek < 0:
            raise ValueError("Napiwek nie może być ujemny")

        self.platnosc = metoda
        self.napiwek = napiwek

    def oblicz_wartosc_zamowienia(self) -> float:
        """
        Oblicza wartość całego zamówienia przed rabatem.

        Returns:
            Wartość zamówienia.
        """
        return sum(pozycja.oblicz_wartosc()
                   for pozycja in self.pozycje.values())

    def oblicz_wartosc_po_rabacie(self) -> float:
        """
        Oblicza wartość zamówienia po uwzględnieniu rabatu.

        Returns:
            Wartość zamówienia po rabacie.
        """
        wartosc = self.oblicz_wartosc_zamowienia()
        return round(wartosc * (1 - self.rabat_procent / 100), 2)

    def oblicz_calkowity_koszt(self) -> float:
        """
        Oblicza całkowity koszt zamówienia z napiwkiem.

        Returns:
            Całkowity koszt zamówienia.
        """
        return self.oblicz_wartosc_po_rabacie() + self.napiwek

    def czas_realizacji(self) -> Optional[float]:
        """
        Oblicza czas realizacji zamówienia w minutach.

        Returns:
            Czas realizacji w minutach lub None jeśli
            zamówienie nie jest zakończone.
        """
        if self.status not in ["dostarczone", "oplacone"]:
            return None

        teraz = datetime.now()
        delta = teraz - self.czas_zlozenia
        return round(delta.total_seconds() / 60, 1)


class ObslugaZamowien:
    """
    Klasa zarządzająca wszystkimi zamówieniami w restauracji.

    Atrybuty:
        zamowienia (Dict[str, Zamowienie]): Słownik wszystkich zamówień.
        menu: Referencja do obiektu menu restauracji.
        aktywne_zamowienia (List[str]): Lista ID aktywnych zamówień.
        historia_zamowien (List[str]): Lista ID zakończonych zamówień.
        statystyki (StatystykiDict): Statystyki zamówień.
    """

    def __init__(self, menu: Any):
        """
        Inicjalizuje nowy system obsługi zamówień.

        Args:
            menu: Referencja do obiektu menu restauracji.
        """
        self.zamowienia: Dict[str, Zamowienie] = {}
        self.menu = menu
        self.aktywne_zamowienia: List[str] = []
        self.historia_zamowien: List[str] = []
        self.statystyki: StatystykiDict = {
            "liczba_zamowien": 0,
            "suma_wartosci": 0.0,
            "srednia_wartosc": 0.0,
            "najpopularniejsze_danie": "",
            "liczba_sprzedanych_dan": {}
        }

    def utworz_zamowienie(self, numer_stolika: int,
                          kelner: str = "") -> Zamowienie:
        """
        Tworzy nowe zamówienie.

        Args:
            numer_stolika: Numer stolika.
            kelner: Imię kelnera.

        Returns:
            Utworzone zamówienie.
        """
        zamowienie = Zamowienie(numer_stolika, kelner)
        self.zamowienia[zamowienie.id] = zamowienie
        self.aktywne_zamowienia.append(zamowienie.id)
        self.statystyki["liczba_zamowien"] += 1
        return zamowienie

    def dodaj_pozycje_do_zamowienia(self, id_zamowienia: str,
                                    nazwa_dania: str, ilosc: int = 1,
                                    uwagi: str = "") -> None:
        """
        Dodaje pozycję do istniejącego zamówienia.

        Args:
            id_zamowienia: ID zamówienia.
            nazwa_dania: Nazwa dania.
            ilosc: Liczba porcji.
            uwagi: Dodatkowe uwagi.

        Raises:
            KeyError: Gdy zamówienie o podanym ID nie istnieje.
            KeyError: Gdy danie o podanej nazwie nie istnieje w menu.
            ValueError: Gdy danie nie jest dostępne.
        """
        if id_zamowienia not in self.zamowienia:
            raise KeyError(f"Zamówienie o ID {id_zamowienia} nie istnieje")

        if nazwa_dania not in self.menu.dania:
            raise KeyError(f"Danie {nazwa_dania} nie istnieje w menu")

        danie = self.menu.dania[nazwa_dania]
        if not danie.dostepne:
            raise ValueError(f"Danie {nazwa_dania} nie jest obecnie dostępne")

        zamowienie = self.zamowienia[id_zamowienia]
        zamowienie.dodaj_pozycje(nazwa_dania, danie.cena, ilosc, uwagi)

        # Aktualizacja statystyk
        liczba_dan = self.statystyki["liczba_sprzedanych_dan"]
        if nazwa_dania in liczba_dan:
            liczba_dan[nazwa_dania] += ilosc
        else:
            liczba_dan[nazwa_dania] = ilosc

        # Aktualizacja najpopularniejszego dania
        if liczba_dan:
            najpop = max(liczba_dan.items(), key=lambda x: x[1])
            self.statystyki["najpopularniejsze_danie"] = najpop[0]

    def usun_pozycje_z_zamowienia(self, id_zamowienia: str, nazwa_dania: str,
                                  ilosc: Optional[int] = None) -> None:
        """
        Usuwa pozycję z istniejącego zamówienia.

        Args:
            id_zamowienia: ID zamówienia.
            nazwa_dania: Nazwa dania.
            ilosc: Liczba porcji do usunięcia (None = wszystkie).

        Raises:
            KeyError: Gdy zamówienie o podanym ID nie istnieje.
            KeyError: Gdy pozycja o podanej nazwie nie istnieje w zamówieniu.
        """
        if id_zamowienia not in self.zamowienia:
            raise KeyError(f"Zamówienie o ID {id_zamowienia} nie istnieje")

        zamowienie = self.zamowienia[id_zamowienia]

        if nazwa_dania not in zamowienie.pozycje:
            raise KeyError(f"Danie {nazwa_dania} "
                           f"nie znajduje się w zamówieniu")

        stara_ilosc = zamowienie.pozycje[nazwa_dania].ilosc
        zamowienie.usun_pozycje(nazwa_dania, ilosc)

        # Aktualizacja statystyk
        liczba_dan = self.statystyki["liczba_sprzedanych_dan"]
        if nazwa_dania in liczba_dan:
            usuwana_ilosc = stara_ilosc \
                if ilosc is None else min(ilosc, stara_ilosc)
            liczba_dan[nazwa_dania] -= usuwana_ilosc

            # Jeśli ilość spadła do zera, usuwamy z najczęściej sprzedawanych
            if liczba_dan[nazwa_dania] <= 0:
                del liczba_dan[nazwa_dania]

            # Aktualizacja najpopularniejszego dania
            if liczba_dan:
                najpop = max(liczba_dan.items(), key=lambda x: x[1])
                self.statystyki["najpopularniejsze_danie"] = najpop[0]
            else:
                self.statystyki["najpopularniejsze_danie"] = ""

    def zamknij_zamowienie(self, id_zamowienia: str,
                           metoda_platnosci: str, napiwek: float = 0) -> float:
        """
        Zamyka zamówienie i przenosi je do historii.

        Args:
            id_zamowienia: ID zamówienia.
            metoda_platnosci: Metoda płatności.
            napiwek: Kwota napiwku.

        Returns:
            Całkowita kwota do zapłaty.

        Raises:
            KeyError: Gdy zamówienie o podanym ID nie istnieje.
            ValueError: Gdy zamówienie nie ma statusu "dostarczone".
        """
        if id_zamowienia not in self.zamowienia:
            raise KeyError(f"Zamówienie o ID {id_zamowienia} nie istnieje")

        zamowienie = self.zamowienia[id_zamowienia]

        if zamowienie.status != "dostarczone":
            raise ValueError("Można zamknąć tylko zamówienie "
                             "o statusie 'dostarczone'")

        zamowienie.ustaw_platnosc(metoda_platnosci, napiwek)
        zamowienie.zmien_status("oplacone")

        # Przenieś do historii
        if id_zamowienia in self.aktywne_zamowienia:
            self.aktywne_zamowienia.remove(id_zamowienia)
        self.historia_zamowien.append(id_zamowienia)

        # Aktualizuj statystyki
        kwota = zamowienie.oblicz_wartosc_po_rabacie()
        self.statystyki["suma_wartosci"] += kwota
        if len(self.historia_zamowien) > 0:
            self.statystyki["srednia_wartosc"] = (
                self.statystyki["suma_wartosci"] / len(self.historia_zamowien)
            )

        return zamowienie.oblicz_calkowity_koszt()

    def anuluj_zamowienie(self, id_zamowienia: str, powod: str = "") -> None:
        """
        Anuluje zamówienie.

        Args:
            id_zamowienia: ID zamówienia.
            powod: Powód anulowania.

        Raises:
            KeyError: Gdy zamówienie o podanym ID nie istnieje.
            ValueError: Gdy zamówienie ma już status "oplacone" lub "anulowane"
        """
        if id_zamowienia not in self.zamowienia:
            raise KeyError(f"Zamówienie o ID {id_zamowienia} nie istnieje")

        zamowienie = self.zamowienia[id_zamowienia]

        if zamowienie.status in ["oplacone", "anulowane"]:
            raise ValueError(f"Nie można anulować zamówienia "
                             f"o statusie '{zamowienie.status}'")

        zamowienie.zmien_status("anulowane")
        zamowienie.uwagi = f"ANULOWANO: {powod}" if powod else "ANULOWANO"

        # Przenieś do historii
        if id_zamowienia in self.aktywne_zamowienia:
            self.aktywne_zamowienia.remove(id_zamowienia)
        self.historia_zamowien.append(id_zamowienia)

        # Cofnij statystyki dań
        liczba_dan = self.statystyki["liczba_sprzedanych_dan"]
        for nazwa_dania, pozycja in zamowienie.pozycje.items():
            if nazwa_dania in liczba_dan:
                liczba_dan[nazwa_dania] -= pozycja.ilosc

                if liczba_dan[nazwa_dania] <= 0:
                    del liczba_dan[nazwa_dania]

        # Aktualizacja najpopularniejszego dania
        if liczba_dan:
            najpop = max(liczba_dan.items(), key=lambda x: x[1])
            self.statystyki["najpopularniejsze_danie"] = najpop[0]
        else:
            self.statystyki["najpopularniejsze_danie"] = ""

    def znajdz_zamowienia_dla_stolika(self,
                                      numer_stolika: int) -> List[Zamowienie]:
        """
        Znajduje wszystkie aktywne zamówienia dla danego stolika.

        Args:
            numer_stolika: Numer stolika.

        Returns:
            Lista aktywnych zamówień dla stolika.
        """
        return [self.zamowienia[id_zam] for id_zam in self.aktywne_zamowienia
                if self.zamowienia[id_zam].numer_stolika == numer_stolika]
