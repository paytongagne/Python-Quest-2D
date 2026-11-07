class SensorFault(ValueError):
    pass

class Sensor:
    def __init__(self, low, high):
        self.low, self.high = low, high

    def read(self, value):
        if not self.low <= value <= self.high:
            raise SensorFault("Outside sensor limits")
        return value
