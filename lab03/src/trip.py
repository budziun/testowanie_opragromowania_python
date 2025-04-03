class Trip:
    def __init__(self,destination,duration):
        self.destination = destination
        self.duration = duration
        self.participants = []

    def calculate_cost(self):
        koszt_dnia = 100
        return self.duration * koszt_dnia

    def add_participant(self, participants):
        if participants.strip() == "":
            raise ValueError("Puste pole - nie można dodać do wycieczki")
        if participants in self.participants:
            raise ValueError(f"Uczestnik {participants} jest już zapisany na wycieczkę")
        self.participants.append(participants)
        print(f"{participants} dodany do wycieczki: {self.destination}")
