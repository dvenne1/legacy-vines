class SeasonSimulator:
    """Handles one season's simulation. Formula-based (easy to expand)."""
    def __init__(self):
        self.year = 1850  # starting era

    def simulate_harvest(self, grid):
        total_yield = 0
        for row in grid:
            for plot in row:
                if plot.varietal:
                    # Simple formula (we'll make it JSON-driven later)
                    yield_this_plot = 50 * (plot.health / 100)
                    total_yield += yield_this_plot
                    print(f"Plot ({plot.x},{plot.y}) yielded {yield_this_plot:.1f} units")
        print(f"Total harvest this season: {total_yield:.1f} units")
        self.year += 1