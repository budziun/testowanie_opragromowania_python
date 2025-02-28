import unittest
from Tools.scripts.make_ctype import values

from src.person import Person

class TestPerson(unittest.TestCase):

    def setUp(self):
        # Ten kod jest wykonywany przed każdym testem
        self.person = Person("Jan","Kowalski",19)

    def test_get_full_name(self):
        #Sprawdzamy czy metoda get_full_name zwraca poprawne imie i nazwisko
        self.assertEqual(self.person.get_full_name(),"Jan Kowalski")
    def test_is_adult_true(self):
        #Sprawdzamy czy meotda is_adult_true zwraca wartosc True dla osób wiek=>18
        self.assertTrue(self.person.is_adult())
    def test_is_adult_false(self):
        # Sprawdzamy, czy metoda is_adult zwraca False dla osoby niepełnoletniej
        new1 = Person("Kajetan","Kajetanowicz",14)
        self.assertFalse(new1.is_adult())
    def test_is_adult_no_age(self):
        # Sprawdzanie czy metoda is_adult posiada wiek do testowania z osoby
        new2 = Person("Andrzej","Duda")
        with self.assertRaises(ValueError):
            new2.is_adult()
    def test_celebrate_birthday(self):
        # Sprawdzamy, czy metoda celebrate_birthday zwiększa wiek o 1
        old_age = self.person.age
        new_age = self.person.celebrate_birthday()
        self.assertEqual(new_age, old_age + 1)
        self.assertEqual(self.person.age, old_age + 1)

    def tearDown(self):
        # Ten kod jest wykonywany po każdym teście
        pass
if __name__ == "__main__":
    unittest.main()