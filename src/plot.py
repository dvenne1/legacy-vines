class Plot:
    """Represents one vineyard tile. Data-driven and expandable."""
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.varietal = None      # will come from JSON later
        self.health = 100
        self.age = 0

    def plant(self, varietal_name):
        self.varietal = varietal_name
        self.age = 0
        self.health = 100
        print(f"Planted {varietal_name} at ({self.x}, {self.y})")  # learning output