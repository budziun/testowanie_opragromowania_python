import unittest
from src.trip import Trip

class TestTripInitialization(unittest.TestCase):
    def setUp(self):
        pass
    def test_initiliziation(self):
        trip1 = Trip("Paris",7)
        self.assertEqual(trip1.duration,7)
        self.assertEqual(trip1.destination,"Paris")
    def test_calculate_cost(self):
        trip1 = Trip("Paryż",7)
        trip2 = Trip("Rzym", 5)
        self.assertEqual(trip1.calculate_cost(),700)
        self.assertEqual(trip2.calculate_cost(),500)
    def test_add_participant(self):
        trip = Trip("Kikół",7)
        trip.add_participant("John")
        self.assertIn("John",trip.participants)
    def test_add_multiply_participant(self):
        trip1 = Trip("Choroszcz",10)
        trip1.add_participant("John")
        trip1.add_participant("Alice")
        trip1.add_participant("Bob")
        self.assertIn("John",trip1.participants)
        self.assertIn("Alice", trip1.participants)
        self.assertIn("Bob", trip1.participants)
        self.assertNotIn("Stefan",trip1.participants)
    def test_add_empty_participant(self):
        trip2 = Trip("Świecie", 14)
        with self.assertRaises(ValueError) as c:
            trip2.add_participant(" ")
        self.assertEqual(str(c.exception),"Puste pole - nie można dodać do wycieczki")
    def test_calculate_cost_zero(self):
        trip = Trip("Grudziądz",0)
        self.assertEqual(trip.calculate_cost(),0)
    def test_add_one_participant_mulitple(self):
        trip = Trip("Olsztyn", 21)
        trip.add_participant("John")
        trip.add_participant("Bob")
        trip.add_participant("Mathew")
        with self.assertRaises(ValueError) as context:
            trip.add_participant("John")
        self.assertEqual(str(context.exception), "Uczestnik John jest już zapisany na wycieczkę")
        self.assertEqual(trip.participants.count("John"), 1)
    def tearDown(self):
        pass

if __name__ == "__main__":
    unittest.main()