"""
Moduł zarządzający menu restauracji.
Zawiera klasy do obsługi dań, kategorii oraz całego menu.

Kod aplikacji z modułu menu_management.py wygenerwoany przy użyciu Claude.ai
model Claude Sonnet 3.7
"""

from typing import List, Optional, Dict, Set
from datetime import datetime


class Danie:
    """
    Klasa reprezentująca pojedyncze danie w menu restauracji.

    Atrybuty:
        nazwa (str): Unikalna nazwa dania.
        cena (float): Cena dania w PLN.
        kategoria (str): Kategoria dania (np. przystawka, zupa, danie główne).
        czas_przygotowania (int): Przybliżony czas przygotowania w minutach.
        dostepne (bool): Czy danie jest obecnie dostępne.
        skladniki (List[str]): Lista głównych składników dania.
        kalorie (Optional[int]): Liczba kalorii lub None jeśli nieznana.
        data_dodania (datetime): Data dodania dania do menu.
    """

    def __init__(self, nazwa: str, cena: float,
                 kategoria: str, czas_przygotowania: int = 30,
                 skladniki: Optional[List[str]] = None,
                 kalorie: Optional[int] = None):
        """
        Inicjalizuje nowe danie w menu.

        Args:
            nazwa: Unikalna nazwa dania.
            cena: Cena dania w PLN (>0).
            kategoria: Kategoria dania.
            czas_przygotowania: Czas przygotowania w minutach.
            skladniki: Lista głównych składników dania.
            kalorie: Liczba kalorii lub None jeśli nieznana.

        Raises:
            ValueError: Gdy cena jest ujemna lub równa zero.
        """
        if cena <= 0:
            raise ValueError("Cena dania musi być większa od zera")

        self.nazwa = nazwa
        self.cena = cena
        self.kategoria = kategoria
        self.czas_przygotowania = czas_przygotowania
        self.dostepne = True
        self.skladniki = skladniki or []
        self.kalorie = kalorie
        self.data_dodania = datetime.now()

    def zmien_cene(self, nowa_cena: float) -> None:
        """
        Zmienia cenę dania.

        Args:
            nowa_cena: Nowa cena dania (>0).

        Raises:
            ValueError: Gdy nowa cena jest ujemna lub równa zero.
        """
        if nowa_cena <= 0:
            raise ValueError("Cena musi być większa od zera")
        self.cena = nowa_cena

    def ustaw_dostepnosc(self, dostepne: bool) -> None:
        """
        Ustawia dostępność dania w menu.

        Args:
            dostepne: Czy danie ma być dostępne.
        """
        self.dostepne = dostepne

    def dodaj_skladnik(self, skladnik: str) -> None:
        """
        Dodaje składnik do dania.

        Args:
            skladnik: Nazwa składnika do dodania.

        Raises:
            ValueError: Gdy składnik już istnieje w daniu.
        """
        if skladnik in self.skladniki:
            raise ValueError(f"Składnik {skladnik} już jest częścią dania")
        self.skladniki.append(skladnik)

    def usun_skladnik(self, skladnik: str) -> None:
        """
        Usuwa składnik z dania.

        Args:
            skladnik: Nazwa składnika do usunięcia.

        Raises:
            ValueError: Gdy składnik nie istnieje w daniu.
        """
        if skladnik not in self.skladniki:
            raise ValueError(f"Składnik {skladnik} nie jest częścią dania")
        self.skladniki.remove(skladnik)


class Menu:
    """
    Klasa reprezentująca całe menu restauracji.

    Atrybuty:
        dania (Dict[str, Danie]): Słownik dań (nazwa: obiekt dania).
        kategorie (Set[str]): Zbiór wszystkich kategorii w menu.
        dania_dnia (List[Danie]): Lista dań dnia.
        max_dania_dnia (int): Maksymalna liczba dań dnia.
        data_aktualizacji (datetime): Data ostatniej aktualizacji menu.
    """

    def __init__(self, max_dania_dnia: int = 3):
        """
        Inicjalizuje nowe puste menu.

        Args:
            max_dania_dnia: Maksymalna liczba dań dnia.

        Raises:
            ValueError: Gdy max_dania_dnia jest mniejsze od 1.
        """
        if max_dania_dnia < 1:
            raise ValueError("Maksymalna liczba dań"
                             " dnia musi być większa od 0")

        self.dania: Dict[str, Danie] = {}
        self.kategorie: Set[str] = set()
        self.dania_dnia: List[Danie] = []
        self.max_dania_dnia = max_dania_dnia
        self.data_aktualizacji = datetime.now()

    def dodaj_danie(self, danie: Danie) -> None:
        """
        Dodaje danie do menu.

        Args:
            danie: Obiekt dania do dodania.

        Raises:
            ValueError: Gdy danie o takiej nazwie już istnieje w menu.
        """
        if danie.nazwa in self.dania:
            raise ValueError(f"Danie o nazwie {danie.nazwa} "
                             f"już istnieje w menu")
        self.dania[danie.nazwa] = danie
        self.kategorie.add(danie.kategoria)
        self.data_aktualizacji = datetime.now()

    def usun_danie(self, nazwa: str) -> None:
        """
        Usuwa danie z menu.

        Args:
            nazwa: Nazwa dania do usunięcia.

        Raises:
            KeyError: Gdy danie o podanej nazwie nie istnieje w menu.
        """
        if nazwa not in self.dania:
            raise KeyError(f"Danie o nazwie {nazwa} nie istnieje w menu")

        # Usuń z dań dnia jeśli było
        if self.dania[nazwa] in self.dania_dnia:
            self.dania_dnia.remove(self.dania[nazwa])

        kategoria_usuwanego = self.dania[nazwa].kategoria
        del self.dania[nazwa]

        # Sprawdź czy to była ostatnia kategoria
        if not any(d.kategoria == kategoria_usuwanego
                   for d in self.dania.values()):
            self.kategorie.remove(kategoria_usuwanego)

        self.data_aktualizacji = datetime.now()

    def znajdz_dania_po_kategorii(self, kategoria: str) -> List[Danie]:
        """
        Znajduje wszystkie dania należące do danej kategorii.

        Args:
            kategoria: Kategoria dań do znalezienia.

        Returns:
            Lista dań należących do danej kategorii.
        """
        return [danie for danie in self.dania.values()
                if danie.kategoria == kategoria]

    def znajdz_dania_w_cenie(self, min_cena: float,
                             max_cena: float) -> List[Danie]:
        """
        Znajduje wszystkie dostępne dania w podanym przedziale cenowym.

        Args:
            min_cena: Minimalna cena dania.
            max_cena: Maksymalna cena dania.

        Returns:
            Lista dostępnych dań w podanym przedziale cenowym.

        Raises:
            ValueError: Gdy min_cena jest większa od max_cena.
        """
        if min_cena > max_cena:
            raise ValueError("Minimalna cena "
                             "nie może być większa od maksymalnej")

        return [danie for danie in self.dania.values()
                if min_cena <= danie.cena <= max_cena and danie.dostepne]

    def dodaj_danie_dnia(self, nazwa: str) -> None:
        """
        Dodaje danie do listy dań dnia.

        Args:
            nazwa: Nazwa dania do dodania.

        Raises:
            KeyError: Gdy danie o podanej nazwie nie istnieje w menu.
            ValueError: Gdy danie jest już na liście dań dnia
            lub lista jest pełna.
        """
        if nazwa not in self.dania:
            raise KeyError(f"Danie o nazwie {nazwa} nie istnieje w menu")

        danie = self.dania[nazwa]

        if danie in self.dania_dnia:
            raise ValueError(f"Danie {nazwa} jest już na liście dań dnia")

        if len(self.dania_dnia) >= self.max_dania_dnia:
            raise ValueError(f"Lista dań dnia jest pełna "
                             f"(max: {self.max_dania_dnia})")

        self.dania_dnia.append(danie)

    def usun_danie_dnia(self, nazwa: str) -> None:
        """
        Usuwa danie z listy dań dnia.

        Args:
            nazwa: Nazwa dania do usunięcia.

        Raises:
            KeyError: Gdy danie o podanej nazwie nie istnieje w menu.
            ValueError: Gdy danie nie jest na liście dań dnia.
        """
        if nazwa not in self.dania:
            raise KeyError(f"Danie o nazwie {nazwa} nie istnieje w menu")

        danie = self.dania[nazwa]

        if danie not in self.dania_dnia:
            raise ValueError(f"Danie {nazwa} nie jest na liście dań dnia")

        self.dania_dnia.remove(danie)
