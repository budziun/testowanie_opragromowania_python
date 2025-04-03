class Sport:
    def __init__(self,name,duration):
        self._equipment = []
        self._calories_per_minute = 10
        self.name = name
        self.duration = duration

    @property
    def name(self):
        return self._name
    @name.setter
    def name(self,value):
        if not isinstance(value,str):
            raise TypeError("Name must be a string")
        if value == "":
            raise ValueError("Name cannot be empty")
        self._name = value

    @property
    def duration(self):
        return self._duration

    @duration.setter
    def duration(self,value):
        if not isinstance(value,int):
            raise TypeError("Duration must be an integer")
        if value <= 0:
            raise ValueError("Duration must be greater than 0")
        self._duration = value

    @property
    def equipment(self):
        return self._equipment.copy()

    @property
    def calories_per_minute(self):
        return self._calories_per_minute

    @calories_per_minute.setter
    def calories_per_minute(self, value):
        if not isinstance(value, (int, float)):
            raise TypeError("Calories per minute must be a number")
        if value <= 0:
            raise ValueError("Calories per minute must be greater than 0")
        self._calories_per_minute = value

    def calculate_calories(self):
        return self.duration * self.calories_per_minute

    def add_equipment(self, equipment):
        if not isinstance(equipment, str):
            raise TypeError("Equipment name must be a string")
        if equipment.strip() == "":
            raise ValueError("Equipment name cannot be empty")

        self._equipment.append(equipment)