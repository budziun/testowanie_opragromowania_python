import pytest
from src.calculator import calculate_discounted_price

# Funkcja do testowania
def calculate_discounted_price(price, discount):
    """
    Calculate price after applying discount.
    Args:
        price (float): Base price
        discount (float): Discount as percentage (0-100)
    Returns:
        float: Price after discount
    """
    if not isinstance(price, (int, float)) or price < 0:
        raise ValueError("Price must be a non-negative number")
    if not isinstance(discount, (int, float)) or discount < 0 or discount > 100:
        raise ValueError("Discount must be a number between 0 and 100")
    discounted_price = price * (1 - discount / 100)
    return round(discounted_price, 2)


# 1. Testy poprawnych obliczeń
@pytest.mark.parametrize("price, discount, expected", [
    (100, 0, 100.00),
    (100, 25, 75.00),
    (200, 50, 100.00),
    (100, 100, 0.00),
    (99.99, 10, 89.99)
])
def test_calculate_discounted_price_valid(price, discount, expected):
    assert calculate_discounted_price(price, discount) == expected

# 2. Testy obsługi nieprawidłowych danych wejściowych
@pytest.mark.parametrize("price, discount", [
    (-10, 10),            # cena ujemna
    ("100", 10),          # cena jako string
    (100, "10"),          # rabat jako string
    (100, -5),            # rabat ujemny
    (100, 150),           # rabat powyżej 100
    (None, 10),           # None jako cena
    (100, None),          # None jako rabat
])
def test_calculate_discounted_price_invalid_input(price, discount):
    with pytest.raises(ValueError):
        calculate_discounted_price(price, discount)

# 3. Test zaokrąglania
def test_calculate_discounted_price_rounding():
    assert calculate_discounted_price(99.99, 33.333) == 66.66