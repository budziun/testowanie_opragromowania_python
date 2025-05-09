"""
Moduł zarządzający stanem magazynowym restauracji.
Zawiera klasy do obsługi składników, przepisów i zarządzania zapasami.

Kod aplikacji z modułu inventory_control.py wygenerwoany przy użyciu Claude.ai
model Claude Sonnet 3.7
"""

from datetime import datetime
from typing import Dict, List, Optional, Tuple
import uuid


class Skladnik:
    """
    Klasa reprezentująca składnik używany w restauracji.

    Atrybuty:
        nazwa (str): Unikalna nazwa składnika.
        jednostka (str): Jednostka miary (np. kg, l, szt).
        ilosc_na_stanie (float): Aktualna ilość na stanie.
        min_ilosc (float): Minimalna wymagana ilość.
        cena_jednostkowa (float): Cena za jednostkę.
        data_waznosci (Optional[datetime]): Data ważności składnika.
        dostawca (str): Nazwa dostawcy.
        kategoria (str): Kategoria składnika (np. mięso, warzywa).
        lokalizacja (str): Miejsce przechowywania w magazynie.
    """

    def __init__(self, nazwa: str, jednostka: str, ilosc_na_stanie: float = 0,
                 min_ilosc: float = 10, cena_jednostkowa: float = 0,
                 data_waznosci: Optional[datetime] = None,
                 dostawca: str = "", kategoria: str = "",
                 lokalizacja: str = ""):
        """
        Inicjalizuje nowy składnik.

        Args:
            nazwa: Unikalna nazwa składnika.
            jednostka: Jednostka miary.
            ilosc_na_stanie: Aktualna ilość na stanie.
            min_ilosc: Minimalna wymagana ilość.
            cena_jednostkowa: Cena za jednostkę.
            data_waznosci: Data ważności składnika.
            dostawca: Nazwa dostawcy.
            kategoria: Kategoria składnika.
            lokalizacja: Miejsce przechowywania w magazynie.

        Raises:
            ValueError: Gdy ilość na stanie, minimalna ilość
            lub cena jednostkowa są ujemne.
        """
        if ilosc_na_stanie < 0:
            raise ValueError("Ilość na stanie nie może być ujemna")
        if min_ilosc < 0:
            raise ValueError("Minimalna ilość nie może być ujemna")
        if cena_jednostkowa < 0:
            raise ValueError("Cena jednostkowa nie może być ujemna")

        self.nazwa = nazwa
        self.jednostka = jednostka
        self.ilosc_na_stanie = ilosc_na_stanie
        self.min_ilosc = min_ilosc
        self.cena_jednostkowa = cena_jednostkowa
        self.data_waznosci = data_waznosci
        self.dostawca = dostawca
        self.kategoria = kategoria
        self.lokalizacja = lokalizacja
        self.historia_zmian = []  # [(datetime, operacja, ilosc)]

        # Zapisz początkowy stan
        if ilosc_na_stanie > 0:
            self.historia_zmian.append((datetime.now(),
                                        "początkowy stan", ilosc_na_stanie))

    def dodaj_zapas(self, ilosc: float, dostawa_id: str = "") -> None:
        """
        Dodaje zapas składnika.

        Args:
            ilosc: Ilość do dodania.
            dostawa_id: Identyfikator dostawy.

        Raises:
            ValueError: Gdy ilość jest ujemna lub zero.
        """
        if ilosc <= 0:
            raise ValueError("Ilość musi być większa od zera")

        self.ilosc_na_stanie += ilosc
        operacja = f"dostawa {dostawa_id}" if dostawa_id else "dostawa"
        self.historia_zmian.append((datetime.now(), operacja, ilosc))

    def zuzyj(self, ilosc: float, cel: str = "") -> None:
        """
        Zużywa składnik.

        Args:
            ilosc: Ilość do zużycia.
            cel: Cel zużycia.

        Raises:
            ValueError: Gdy ilość jest ujemna lub zero.
            ValueError: Gdy na stanie jest za mało składnika.
        """
        if ilosc <= 0:
            raise ValueError("Ilość musi być większa od zera")

        if ilosc > self.ilosc_na_stanie:
            raise ValueError(f"Za mało składnika {self.nazwa} na stanie")

        self.ilosc_na_stanie -= ilosc
        operacja = f"zużycie {cel}" if cel else "zużycie"
        self.historia_zmian.append((datetime.now(), operacja, -ilosc))

    def zmien_cene(self, nowa_cena: float) -> None:
        """
        Zmienia cenę jednostkową składnika.

        Args:
            nowa_cena: Nowa cena jednostkowa.

        Raises:
            ValueError: Gdy nowa cena jest ujemna.
        """
        if nowa_cena < 0:
            raise ValueError("Cena nie może być ujemna")

        self.cena_jednostkowa = nowa_cena

    def ustaw_date_waznosci(self, data_waznosci: datetime) -> None:
        """
        Ustawia datę ważności składnika.

        Args:
            data_waznosci: Nowa data ważności.

        Raises:
            ValueError: Gdy data ważności jest w przeszłości.
        """
        if data_waznosci < datetime.now():
            raise ValueError("Data ważności nie może być w przeszłości")

        self.data_waznosci = data_waznosci

    def czy_wymaga_zamowienia(self) -> bool:
        """
        Sprawdza czy składnik wymaga zamówienia.

        Returns:
            True jeśli ilość na stanie jest mniejsza
             od minimalnej wymaganej ilości.
        """
        return self.ilosc_na_stanie < self.min_ilosc

    def czy_przeterminowany(self) -> bool:
        """
        Sprawdza czy składnik jest przeterminowany.

        Returns:
            True jeśli składnik jest przeterminowany, False jeśli nie lub
            data ważności nie jest ustawiona.
        """
        if self.data_waznosci is None:
            return False

        return datetime.now() > self.data_waznosci

    def wartosc_zapasu(self) -> float:
        """
        Oblicza wartość zapasu składnika.

        Returns:
            Wartość zapasu (ilość * cena jednostkowa).
        """
        return round(self.ilosc_na_stanie * self.cena_jednostkowa, 2)


class ZarzadzanieSkladnikami:
    """
    Klasa zarządzająca wszystkimi składnikami i przepisami w restauracji.

    Atrybuty:
        skladniki (Dict[str, Skladnik]): Słownik składników.
        przepisy (Dict[str, Dict[str, float]]): Słownik przepisów.
        dostawy (List[Dict]): Lista wszystkich dostaw.
        kategorie_skladnikow (Set[str]): Zbiór wszystkich kategorii składników.
        dostawcy (Set[str]): Zbiór wszystkich dostawców.
    """

    def __init__(self):
        """
        Inicjalizuje nowy system zarządzania składnikami.
        """
        self.skladniki = {}
        self.przepisy = {}  # nazwa_dania: {nazwa_skladnika: ilosc, ...}
        self.dostawy = []
        self.kategorie_skladnikow = set()
        self.dostawcy = set()

    def dodaj_skladnik(self, skladnik: Skladnik):
        """
        Dodaje składnik do systemu.

        Args:
            skladnik: Obiekt składnika do dodania.

        Raises:
            ValueError: Gdy składnik o takiej nazwie już istnieje.
        """
        if skladnik.nazwa in self.skladniki:
            raise ValueError(f"Składnik {skladnik.nazwa} już istnieje")
        self.skladniki[skladnik.nazwa] = skladnik

        if skladnik.kategoria:
            self.kategorie_skladnikow.add(skladnik.kategoria)

        if skladnik.dostawca:
            self.dostawcy.add(skladnik.dostawca)

    def usun_skladnik(self, nazwa: str):
        """
        Usuwa składnik z systemu.

        Args:
            nazwa: Nazwa składnika do usunięcia.

        Raises:
            KeyError: Gdy składnik o podanej nazwie nie istnieje.
            ValueError: Gdy składnik jest używany w przepisach.
        """
        if nazwa not in self.skladniki:
            raise KeyError(f"Składnik {nazwa} nie istnieje")

        # Sprawdź czy składnik jest używany w przepisach
        for nazwa_dania, skladniki in self.przepisy.items():
            if nazwa in skladniki:
                raise ValueError(
                    f"Nie można usunąć składnika {nazwa}, "
                    f"jest używany w przepisie {nazwa_dania}"
                )

        kategoria = self.skladniki[nazwa].kategoria
        dostawca = self.skladniki[nazwa].dostawca

        del self.skladniki[nazwa]

        # Aktualizuj kategorie i dostawców
        if kategoria:
            if not any(s.kategoria == kategoria
                       for s in self.skladniki.values()):
                self.kategorie_skladnikow.remove(kategoria)

        if dostawca:
            if not any(s.dostawca == dostawca
                       for s in self.skladniki.values()):
                self.dostawcy.remove(dostawca)

    def dodaj_przepis(self, nazwa_dania: str,
                      skladniki_ilosci: Dict[str, float]):
        """
        Dodaje przepis do systemu.

        Args:
            nazwa_dania: Nazwa dania.
            skladniki_ilosci: Słownik z nazwami składników i ich ilościami.

        Raises:
            ValueError: Gdy przepis jest pusty.
            KeyError: Gdy jakiś składnik nie istnieje.
            ValueError: Gdy przepis o takiej nazwie już istnieje.
        """
        if not skladniki_ilosci:
            raise ValueError("Przepis musi zawierać "
                             "przynajmniej jeden składnik")

        for skladnik_nazwa, ilosc in skladniki_ilosci.items():
            if skladnik_nazwa not in self.skladniki:
                raise KeyError(f"Składnik {skladnik_nazwa} nie istnieje")

            if ilosc <= 0:
                raise ValueError(
                    f"Ilość składnika {skladnik_nazwa} "
                    f"musi być większa od zera"
                )

        if nazwa_dania in self.przepisy:
            raise ValueError(f"Przepis dla dania {nazwa_dania} już istnieje")

        self.przepisy[nazwa_dania] = skladniki_ilosci.copy()

    def aktualizuj_przepis(self, nazwa_dania: str,
                           skladniki_ilosci: Dict[str, float]):
        """
        Aktualizuje istniejący przepis.

        Args:
            nazwa_dania: Nazwa dania.
            skladniki_ilosci: Słownik z nazwami składników i ich ilościami.

        Raises:
            KeyError: Gdy przepis o podanej nazwie nie istnieje.
            ValueError: Gdy nowy przepis jest pusty.
            KeyError: Gdy jakiś składnik nie istnieje.
        """
        if nazwa_dania not in self.przepisy:
            raise KeyError(f"Przepis dla dania {nazwa_dania} nie istnieje")

        if not skladniki_ilosci:
            raise ValueError("Przepis musi zawierać "
                             "przynajmniej jeden składnik")

        for skladnik_nazwa, ilosc in skladniki_ilosci.items():
            if skladnik_nazwa not in self.skladniki:
                raise KeyError(f"Składnik {skladnik_nazwa} nie istnieje")

            if ilosc <= 0:
                raise ValueError(
                    f"Ilość składnika {skladnik_nazwa} "
                    f"musi być większa od zera"
                )

        self.przepisy[nazwa_dania] = skladniki_ilosci.copy()

    def usun_przepis(self, nazwa_dania: str):
        """
        Usuwa przepis z systemu.

        Args:
            nazwa_dania: Nazwa dania.

        Raises:
            KeyError: Gdy przepis o podanej nazwie nie istnieje.
        """
        if nazwa_dania not in self.przepisy:
            raise KeyError(f"Przepis dla dania {nazwa_dania} nie istnieje")

        del self.przepisy[nazwa_dania]

    def sprawdz_mozliwosc_przygotowania(self, nazwa_dania: str,
                                        ilosc: int = 1) -> bool:
        """
        Sprawdza możliwość przygotowania dania w podanej ilości.

        Args:
            nazwa_dania: Nazwa dania.
            ilosc: Liczba porcji.

        Returns:
            True jeśli możliwe jest przygotowanie, False w przeciwnym przypadku
        Raises:
            KeyError: Gdy przepis o podanej nazwie nie istnieje.
        """
        if nazwa_dania not in self.przepisy:
            raise KeyError(f"Brak przepisu dla dania {nazwa_dania}")

        for skladnik_nazwa, potrzebna_ilosc in \
                self.przepisy[nazwa_dania].items():
            if skladnik_nazwa not in self.skladniki:
                return False
            if self.skladniki[skladnik_nazwa].ilosc_na_stanie \
                    < potrzebna_ilosc * ilosc:
                return False
        return True

    def przygotuj_danie(self, nazwa_dania: str, ilosc: int = 1):
        """
        Przygotowuje danie, zużywając odpowiednie składniki.

        Args:
            nazwa_dania: Nazwa dania.
            ilosc: Liczba porcji.

        Raises:
            KeyError: Gdy przepis o podanej nazwie nie istnieje.
            ValueError: Gdy nie ma wystarczającej ilości składników.
        """
        if not self.sprawdz_mozliwosc_przygotowania(nazwa_dania, ilosc):
            raise ValueError(
                f"Brak wystarczającej ilości składników "
                f"do przygotowania {nazwa_dania}"
            )

        for skladnik_nazwa, potrzebna_ilosc in self.przepisy[nazwa_dania].\
                items():
            self.skladniki[skladnik_nazwa].zuzyj(
                potrzebna_ilosc * ilosc, nazwa_dania
            )

    def zarejestruj_dostawe(
        self, dostawca: str, pozycje: Dict[str, Tuple[float, float]],
            uwagi: str = "") -> str:
        """
        Rejestruje nową dostawę składników.

        Args:
            dostawca: Nazwa dostawcy.
            pozycje: Słownik z nazwami składników i
            krotkami (ilość, cena jednostkowa).
            uwagi: Dodatkowe uwagi do dostawy.

        Returns:
            ID dostawy.

        Raises:
            KeyError: Gdy jakiś składnik nie istnieje.
        """
        dostawa_id = str(uuid.uuid4())
        czas_dostawy = datetime.now()

        for skladnik_nazwa, (ilosc, cena) in pozycje.items():
            if skladnik_nazwa not in self.skladniki:
                raise KeyError(f"Składnik {skladnik_nazwa} nie istnieje")

            # Aktualizuj stan składnika
            self.skladniki[skladnik_nazwa].dodaj_zapas(ilosc, dostawa_id)

            # Aktualizuj cenę jeśli podano
            if cena > 0:
                self.skladniki[skladnik_nazwa].zmien_cene(cena)

        # Dodaj dostawcę jeśli nowy
        self.dostawcy.add(dostawca)

        # Zapisz dostawę
        dostawa = {
            "id": dostawa_id,
            "dostawca": dostawca,
            "czas_dostawy": czas_dostawy,
            "pozycje": pozycje.copy(),
            "uwagi": uwagi
        }

        self.dostawy.append(dostawa)
        return dostawa_id

    def lista_do_zamowienia(self) -> List[Skladnik]:
        """
        Tworzy listę składników do zamówienia.

        Returns:
            Lista składników, których ilość jest poniżej minimalnej.
        """
        return [
            skladnik for skladnik in self.skladniki.values()
            if skladnik.czy_wymaga_zamowienia()
        ]

    def znajdz_przeterminowane(self) -> List[Skladnik]:
        """
        Znajduje wszystkie przeterminowane składniki.

        Returns:
            Lista przeterminowanych składników.
        """
        return [
            skladnik for skladnik in self.skladniki.values()
            if skladnik.czy_przeterminowany()
        ]

    def oblicz_wartosc_magazynu(self) -> float:
        """
        Oblicza całkowitą wartość magazynu.

        Returns:
            Całkowita wartość wszystkich składników w magazynie.
        """
        return sum(
            skladnik.wartosc_zapasu() for skladnik in self.skladniki.values()
        )
