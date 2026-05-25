import json
from pathlib import Path

class Plot:
    """Represents one vineyard tile. Loads real data from JSON."""
    VARIETIES = None  # loaded once

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.varietal = None
        self.health = 100
        self.age = 0

    @classmethod
    def load_varieties(cls):
        if cls.VARIETIES is None:
            path = Path(__file__).parent.parent / "data" / "vines.json"
            with open(path) as f:
                cls.VARIETIES = json.load(f)
        return cls.VARIETIES

    def plant(self, varietal_name):
        varieties = self.load_varieties()
        if varietal_name in varieties:
            self.varietal = varietal_name
            self.age = 0
            self.health = 100
            print(f"Planted {varietal_name} at ({self.x}, {self.y})")
        else:
            print(f"Unknown variety: {varietal_name}")
            