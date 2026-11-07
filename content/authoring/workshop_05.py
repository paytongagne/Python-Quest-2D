class Rover:
    def __init__(self, name):
        self.name = name

class SurveyRover(Rover):
    def report(self):
        return {"name": self.name, "role": "survey"}

class CargoRover(Rover):
    def report(self):
        return {"name": self.name, "role": "cargo"}
