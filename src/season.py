from plot import Plot

class SeasonSimulator:
    def __init__(self):
        self.year = 1850

    def simulate_harvest(self, grid, tech_bonus=1.0, aging_multiplier=1.0):
        """Now respects heir traits (Traditionalist = extra aging bonus)."""
        total_yield = 0
        varieties = Plot.load_varieties()
        for row in grid:
            for plot in row:
                if plot.varietal:
                    data = varieties[plot.varietal]
                    age_bonus = 1.0 + (plot.age * 0.08) * aging_multiplier
                    if age_bonus > 1.4:
                        age_bonus = 1.4
                    
                    yield_this_plot = (data["base_yield"] * (plot.health / 100) 
                                       * tech_bonus * age_bonus)
                    
                    total_yield += yield_this_plot
                    print(f"Plot ({plot.x},{plot.y}) {plot.varietal} (age {plot.age}) "
                          f"yielded {yield_this_plot:.1f} units")
                    
                    plot.age += 1
        print(f"Total harvest this season: {total_yield:.1f} units "
              f"(tech x{tech_bonus:.1f} + aging x{aging_multiplier:.1f})")
        self.year += 1