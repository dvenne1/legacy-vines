from plot import Plot

class SeasonSimulator:
    def __init__(self):
        self.year = 1850

    def simulate_harvest(self, grid, tech_bonus=1.0):
        """Now includes vine aging bonus."""
        total_yield = 0
        varieties = Plot.load_varieties()
        for row in grid:
            for plot in row:
                if plot.varietal:
                    data = varieties[plot.varietal]
                    age_bonus = 1.0 + (plot.age * 0.08)  # +8% per year of age, up to ~40%
                    if age_bonus > 1.4:
                        age_bonus = 1.4
                    
                    yield_this_plot = (data["base_yield"] * (plot.health / 100) 
                                       * tech_bonus * age_bonus)
                    
                    total_yield += yield_this_plot
                    print(f"Plot ({plot.x},{plot.y}) {plot.varietal} (age {plot.age}) "
                          f"yielded {yield_this_plot:.1f} units")
                    
                    # Age the vine for next season
                    plot.age += 1
        print(f"Total harvest this season: {total_yield:.1f} units "
              f"(tech x{tech_bonus:.1f} + aging)")
        self.year += 1