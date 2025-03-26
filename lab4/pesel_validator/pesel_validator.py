import re
from datetime import datetime


class PeselValidator:
    """Klasa do walidacji numerów PESEL zgodnie z oficjalnymi zasadami.

    Zawiera metody do sprawdzania poprawności formatu, sumy kontrolnej,
    daty urodzenia oraz określania płci na podstawie numeru PESEL.
    """

    @staticmethod
    def validate_format(pesel):
        """Sprawdza czy PESEL ma prawidłowy format.

        Args:
            pesel (str): Numer PESEL do walidacji

        Returns:
            bool: True jeśli PESEL ma 11 cyfr, False w przeciwnym wypadku
        """
        return bool(re.match(r'^\d{11}$', pesel))

    @staticmethod
    def validate_check_digit(pesel):
        """Waliduje sumę kontrolną numeru PESEL.

        Args:
            pesel (str): Numer PESEL do walidacji

        Returns:
            bool: True jeśli suma kontrolna jest prawidłowa, False w przeciwnym wypadku

        Note:
            Algorytm obliczania sumy kontrolnej:
            1. Mnożymy każdą z pierwszych 10 cyfr przez odpowiednią wagę: 1,3,7,9,1,3,7,9,1,3
            2. Sumujemy wyniki mnożeń
            3. Obliczamy resztę z dzielenia sumy przez 10
            4. Jeśli reszta != 0, odejmujemy ją od 10
            5. Otrzymany wynik powinien być równy 11 cyfrze PESEL
        """
        weights = [1, 3, 7, 9, 1, 3, 7, 9, 1, 3]
        total = sum(int(pesel[i]) * weights[i] for i in range(10))
        check_digit = (10 - (total % 10)) % 10
        return int(pesel[10]) == check_digit

    @staticmethod
    def validate_birth_date(pesel):
        """Sprawdza czy data urodzenia zakodowana w PESEL jest prawidłowa.

        Args:
            pesel (str): Numer PESEL do walidacji

        Returns:
            bool: True jeśli data jest prawidłowa i nie jest z przyszłości, False w przeciwnym wypadku

        Note:
            Format daty w PESEL:
            - RR - ostatnie dwie cyfry roku
            - MM - miesiąc z zakodowanym wiekiem:
              * +20 dla lat 2000-2099
              * +40 dla lat 2100-2199
              * +60 dla lat 2200-2299
              * +80 dla lat 1800-1899
            - DD - dzień
        """
        year = int(pesel[0:2])
        month = int(pesel[2:4])
        day = int(pesel[4:6])

        century_code = month // 20
        month %= 20

        full_year = {
            0: 1900,
            1: 2000,
            2: 2100,
            3: 2200,
            4: 1800
        }.get(century_code, 1900)

        year += full_year

        try:
            birth_date = datetime(year, month, day)
            current_year = datetime.now().year
            return birth_date.year <= current_year
        except ValueError:
            return False

    @staticmethod
    def get_gender(pesel):
        """Określa płeć na podstawie numeru PESEL.

        Args:
            pesel (str): Numer PESEL

        Returns:
            str: 'male' dla mężczyzny, 'female' dla kobiety

        Note:
            Płeć określana jest na podstawie przedostatniej cyfry:
            - Nieparzysta → mężczyzna
            - Parzysta → kobieta
        """
        gender_digit = int(pesel[9])
        return 'male' if gender_digit % 2 == 1 else 'female'

    @staticmethod
    def is_valid(pesel):
        """Kompleksowa walidacja numeru PESEL.

        Args:
            pesel (str): Numer PESEL do walidacji

        Returns:
            bool: True jeśli PESEL jest prawidłowy (format, suma kontrolna i data), False w przeciwnym wypadku
        """
        return (
                PeselValidator.validate_format(pesel) and
                PeselValidator.validate_check_digit(pesel) and
                PeselValidator.validate_birth_date(pesel)
        )