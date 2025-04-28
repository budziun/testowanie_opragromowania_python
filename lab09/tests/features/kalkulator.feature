# language: pl
Właściwość: Podstawowe operacje kalkulatora
  Jako użytkownik kalkulatora
  Chcę wykonywać podstawowe operacje matematyczne
  Aby móc szybko obliczać wyniki

  Szablon scenariusza: Dodawanie dwóch liczb
    Mając kalkulator
    Kiedy wprowadzę liczbę <liczba1>
    I wprowadzę liczbę <liczba2>
    I wybiorę operację dodawania
    Wtedy wynik powinien wynosić <wynik>

    Przykłady:
      | liczba1 | liczba2 | wynik |
      | 2       | 3       | 5     |
      | 10      | 5       | 15    |
      | 0       | 0       | 0     |
      | -5      | 3       | -2    |

  Scenariusz: Odejmowanie dwóch liczb
    Mając kalkulator
    Kiedy wprowadzę liczbę 10
    I wprowadzę liczbę 3
    I wybiorę operację odejmowania
    Wtedy wynik powinien wynosić 7

  Scenariusz: Mnożenie dwóch liczb
    Mając kalkulator
    Kiedy wprowadzę liczbę 4
    I wprowadzę liczbę 5
    I wybiorę operację mnożenia
    Wtedy wynik powinien wynosić 20

  Scenariusz: Dzielenie dwóch liczb
    Mając kalkulator
    Kiedy wprowadzę liczbę 10
    I wprowadzę liczbę 2
    I wybiorę operację dzielenia
    Wtedy wynik powinien wynosić 5

  Scenariusz: Próba dzielenia przez zero
    Mając kalkulator
    Kiedy wprowadzę liczbę 10
    I wprowadzę liczbę 0
    I wybiorę operację dzielenia
    Wtedy powinien zostać zgłoszony błąd "Nie można dzielić przez zero"