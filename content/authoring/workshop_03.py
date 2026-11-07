class Battery:
    def __init__(self, percent):
        self.battery_percent = percent

    @property
    def battery_percent(self):
        return self._percent

    @battery_percent.setter
    def battery_percent(self, value):
        if type(value) not in (int, float):
            raise TypeError("Expected a number")
        if not 0 <= value <= 100:
            raise ValueError("Charge must be 0..100")
        self._percent = value
