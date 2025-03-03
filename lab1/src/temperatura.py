class TemperatureConverter:
    @staticmethod
    def celsius_to_fahrenheit(celsius: float) -> float:
        return (celsius * 9/5) + 32
    @staticmethod
    def fahrenheit_to_celsius(fahrenheit: float) -> float:
        return (fahrenheit - 32) * 5/9
    @staticmethod
    def celsius_to_kelvin(celsius: float) -> float:
        return celsius + 273.15
    @staticmethod
    def kelvin_to_celsius(kelvin: float) -> float:
        return kelvin - 273.15
