from plot import Plot

class SeasonSimulator:
    def __init__(self):
        self.year = 1850

    def simulate_harvest(self, grid, tech_bonus=1.0):
        """tech_bonus = 1.2 when Improved Rootstock is unlocked."""
        total_yield = 0
        varieties = Plot.load_varieties()
        for row in grid:
            for plot in row:
                if plot.varietal:
                    data = varieties[plot.varietal]
                    yield_this_plot = data["base_yield"] * (plot.health / 100) * tech_bonus
                    total_yield += yield_this_plot
                    print(f"Plot ({plot.x},{plot.y}) {plot.varietal} yielded {yield_this_plot:.1f} units")
        print(f"Total harvest this season: {total_yield:.1f} units (tech bonus x{tech_bonus})")
        self.year += 1