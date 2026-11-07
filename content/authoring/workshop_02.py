class Probe:
    def __init__(self, reading):
        self.reading = reading

    def calibrate(self, offset):
        self.reading += offset
        return self.reading
