import re
from datetime import datetime

class PeselValidator:
    @staticmethod
    def validate_format(pesel):
        return bool(re.match(r'^\d{11}$', pesel))

    @staticmethod
    def validate_check_digit(pesel):
        weights = [1, 3, 7, 9, 1, 3, 7, 9, 1, 3]
        total = sum(int(pesel[i]) * weights[i] for i in range(10))
        check_digit = (10 - (total % 10)) % 10
        return int(pesel[10]) == check_digit

    @staticmethod
    def validate_birth_date(pesel):
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
        gender_digit = int(pesel[9])
        return 'male' if gender_digit % 2 == 1 else 'female'

    @staticmethod
    def is_valid(pesel):
        return (
            PeselValidator.validate_format(pesel) and
            PeselValidator.validate_check_digit(pesel) and
            PeselValidator.validate_birth_date(pesel)
        )