import pytest
from src.shopping_cart import ShoppingCart, Product

# --- Fixtures ---
@pytest.fixture
def product_apple():
    return Product(1, "Apple", 2.5)

@pytest.fixture
def product_banana():
    return Product(2, "Banana", 3.0)

@pytest.fixture
def empty_cart():
    return ShoppingCart()

@pytest.fixture
def cart_with_items(product_apple, product_banana):
    cart = ShoppingCart()
    cart.add_product(product_apple, 2)
    cart.add_product(product_banana, 3)
    return cart

# Dodawanie produktów
@pytest.mark.parametrize("quantity", [1, 2, 5])
def test_add_product(empty_cart, product_apple, quantity):
    empty_cart.add_product(product_apple, quantity)
    assert empty_cart.get_product_count() == quantity
    assert product_apple.id in empty_cart.products

# Usuwanie produktów
def test_remove_single_product(cart_with_items, product_apple):
    cart_with_items.remove_product(product_apple.id, 1)
    assert cart_with_items.get_product_count() == 4

def test_remove_entire_product(cart_with_items, product_banana):
    cart_with_items.remove_product(product_banana.id, 3)
    assert product_banana.id not in cart_with_items.products

# Obliczanie całkowitej wartości koszyka
def test_total_price(cart_with_items):
    assert cart_with_items.get_total_price() == round(2.5 * 2 + 3.0 * 3, 2)

# Zliczanie produktów
def test_product_count(cart_with_items):
    assert cart_with_items.get_product_count() == 5

# Obsługa błędów
def test_remove_nonexistent_product_raises(empty_cart):
    with pytest.raises(ValueError):
        empty_cart.remove_product(99)

def test_add_product_with_zero_quantity_raises(product_apple, empty_cart):
    with pytest.raises(ValueError):
        empty_cart.add_product(product_apple, 0)

def test_remove_with_invalid_quantity_raises(cart_with_items):
    with pytest.raises(ValueError):
        cart_with_items.remove_product(1, 0)