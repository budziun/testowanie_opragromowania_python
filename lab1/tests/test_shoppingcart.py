import unittest
from src.shop import ShoppingCart

class TestShoppingCart(unittest.TestCase):
    def setUp(self):
        self.cart = ShoppingCart();
    def test_add_item(self):
        self.cart.add_item("Perła Export",2.69,4)
        self.assertEqual(self.cart.items["Perła Export"],{"price": 2.69,"quantity":4})
    def test_remove_item(self):
        self.cart.add_item("Łomża Pils",3.11,4)
        self.cart.remove_item("Łomża Pils",2)
        self.assertEqual(self.cart.items["Łomża Pils"],{"price":3.11,"quantity":2})
        self.cart.remove_item("Łomża Pils",2)
        self.assertNotIn("Łomża Pils",self.cart.items)
    def test_get_total(self):
        self.cart.add_item("Specjal",1.99,12)
        self.cart.add_item("Harnas",2.99,12)
        self.assertEqual(self.cart.get_total(),60)
    def test_clear(self):
        self.cart.add_item("Kuflowe",1.25,6)
        self.cart.clear()
        self.assertEqual(len(self.cart.items),0)

if __name__ == "__main__":
    unittest.main()