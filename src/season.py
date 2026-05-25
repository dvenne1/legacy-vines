from plot import Plot   # <-- THIS WAS THE MISSING LINE

class SeasonSimulator:
    def __init__(self):
        self.year = 1850

    def simulate_harvest(self, grid):
        total_yield = 0
        varieties = Plot.load_varieties()  # now it can find Plot
        for row in grid:
            for plot in row:
                if plot.varietal:
                    data = varieties[plot.varietal]
                    yield_this_plot = data["base_yield"] * (plot.health / 100)
                    total_yield += yield_this_plot
                    print(f"Plot ({plot.x},{plot.y}) {plot.varietal} yielded {yield_this_plot:.1f} units")
        print(f"Total harvest this season: {total_yield:.1f} units")
        self.year += 1