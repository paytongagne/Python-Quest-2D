class Reservoir:
    def __init__(self, capacity, water, supply):
        self.capacity = capacity
        self.water = water
        self.supply = supply

    def refill(self, amount):
        if amount < 0:
            raise ValueError("Negative transfer")
        moved = min(amount, self.capacity-self.water, self.supply)
        self.water += moved
        self.supply -= moved
        return moved
