class Battery:
    def __init__(self, charge):
        self.charge = charge

    def consume(self, amount):
        if amount < 0 or amount > self.charge:
            raise ValueError("Insufficient charge or negative request")
        self.charge -= amount
        return self.charge

class Rover:
    def __init__(self, battery):
        self.battery = battery

    def drive(self, amount):
        return self.battery.consume(amount)
