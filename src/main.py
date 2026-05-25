import pygame
import sys
from pathlib import Path
import random
import json

sys.path.insert(0, str(Path(__file__).parent))

from plot import Plot
from season import SeasonSimulator

pygame.init()

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Legacy Vines - Prototype")

BLACK = (0, 0, 0)
GREEN = (34, 139, 34)
BROWN = (139, 69, 19)
BUTTON_COLOR = (200, 0, 0)
SELECTED_COLOR = (0, 200, 0)
TECH_COLOR = (0, 100, 200)
GENERATION_COLOR = (139, 0, 139)
HEIR_COLOR = (255, 165, 0)
EVENT_COLOR = (200, 50, 50)
VICTORY_COLOR = (0, 100, 0)

# Game state
grid = [[Plot(x, y) for x in range(5)] for y in range(5)]
simulator = SeasonSimulator()
money = 2500
current_variety = "Nebbiolo"
research_points = 0
unlocked_tech = False
current_generation = 1
legacy_score = 0
heir_trait = "None"
show_heir_choice = False
current_event = None
victory = False

current_market_prices = {}

def load_events():
    path = Path(__file__).parent.parent / "data" / "events.json"
    with open(path) as f:
        return json.load(f)

def update_market_prices():
    varieties = Plot.load_varieties()
    for name, data in varieties.items():
        multiplier = random.uniform(0.7, 1.3)
        current_market_prices[name] = round(data["base_market_price"] * multiplier, 1)

events_list = load_events()
update_market_prices()

clock = pygame.time.Clock()
running = True
font = pygame.font.SysFont(None, 36)
small_font = pygame.font.SysFont(None, 20)
big_font = pygame.font.SysFont(None, 72)

def draw_vineyard_plot(surface, rect, plot):
    if plot.varietal is None:
        pygame.draw.rect(surface, (160, 120, 70), rect)
        for i in range(4):
            y_offset = rect.y + 20 + i * 18
            pygame.draw.line(surface, (120, 90, 50), (rect.x + 10, y_offset), (rect.x + rect.width - 10, y_offset), 2)
        return

    varieties = Plot.load_varieties()
    data = varieties[plot.varietal]
    health_ratio = plot.health / 100.0
    age_factor = min(plot.age / 10.0, 1.0)

    soil_color = (160, 120, 70) if health_ratio > 0.6 else (140, 100, 50)
    pygame.draw.rect(surface, soil_color, rect)

    num_rows = 4
    row_spacing = rect.width // (num_rows + 1)
    vine_green = (34, 139, 34) if health_ratio > 0.5 else (100, 140, 80)
    leaf_density = int(6 * age_factor * health_ratio)

    for i in range(1, num_rows + 1):
        x = rect.x + i * row_spacing
        pygame.draw.line(surface, (80, 50, 30), (x, rect.y + 10), (x, rect.y + rect.height - 10), 3)
        for j in range(leaf_density):
            leaf_y = rect.y + 20 + j * 12
            pygame.draw.line(surface, vine_green, (x - 8, leaf_y), (x + 8, leaf_y), 4)

    if health_ratio < 0.7:
        overlay = pygame.Surface((rect.width, rect.height))
        overlay.set_alpha(int(80 * (1 - health_ratio)))
        overlay.fill((200, 50, 50))
        surface.blit(overlay, (rect.x, rect.y))

    short_name = data.get("short_name", plot.varietal[:4])
    var_text = small_font.render(short_name, True, BLACK)
    screen.blit(var_text, (rect.x + 8, rect.y + 8))
    age_text = small_font.render(f"Age:{plot.age}", True, BLACK)
    screen.blit(age_text, (rect.x + 8, rect.y + 28))
    health_text = small_font.render(f"{int(plot.health)}%", True, BLACK)
    screen.blit(health_text, (rect.x + 8, rect.y + 48))

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()

            if victory:
                if pygame.Rect(400, 500, 200, 60).collidepoint(mx, my):
                    grid = [[Plot(x, y) for x in range(5)] for y in range(5)]
                    simulator = SeasonSimulator()
                    money = 2500
                    current_variety = "Nebbiolo"
                    research_points = 0
                    unlocked_tech = False
                    current_generation = 1
                    legacy_score = 0
                    heir_trait = "None"
                    show_heir_choice = False
                    current_event = None
                    victory = False
                    update_market_prices()
                continue

            # Plant
            for y in range(5):
                for x in range(5):
                    rect = pygame.Rect(x * 120 + 50, y * 120 + 50, 100, 100)
                    if rect.collidepoint(mx, my):
                        varieties = Plot.load_varieties()
                        cost = varieties[current_variety]["cost_to_plant"]
                        if money >= cost:
                            grid[y][x].plant(current_variety)
                            money -= cost
                        else:
                            print("Not enough money to plant!")

            # Variety buttons (moved lower)
            if pygame.Rect(50, 670, 180, 50).collidepoint(mx, my):
                current_variety = "Nebbiolo"
            if pygame.Rect(250, 670, 180, 50).collidepoint(mx, my):
                current_variety = "Chardonnay"
            if pygame.Rect(450, 670, 180, 50).collidepoint(mx, my):
                current_variety = "Cabernet Sauvignon"

            # HARVEST
            if pygame.Rect(700, 50, 200, 60).collidepoint(mx, my):
                tech_bonus = 1.2 if unlocked_tech else 1.0
                aging_multiplier = 1.15 if heir_trait == "Traditionalist" else 1.0
                extra_research = 1 if heir_trait == "Scientist" else 0

                simulator.simulate_harvest(grid, tech_bonus, aging_multiplier)
                research_points += 1 + extra_research

                total_income = 0
                varieties = Plot.load_varieties()
                for row in grid:
                    for plot in row:
                        if plot.varietal:
                            data = varieties[plot.varietal]
                            yield_this_plot = data["base_yield"] * (plot.health / 100) * tech_bonus * aging_multiplier
                            income = yield_this_plot * current_market_prices[plot.varietal]
                            total_income += income
                            money += int(income)

                if random.random() < 0.25:
                    current_event = random.choice(events_list)

                update_market_prices()

                if current_generation >= 5:
                    victory = True

            # RESEARCH
            if pygame.Rect(700, 130, 200, 60).collidepoint(mx, my) and research_points > 0 and money >= 300:
                unlocked_tech = True
                research_points -= 1
                money -= 300

            # END GENERATION
            if pygame.Rect(700, 210, 200, 60).collidepoint(mx, my) and not show_heir_choice:
                legacy_bonus = 1.1 if heir_trait == "Marketer" else 1.0
                legacy_score += int((100 + (simulator.year - 1850) * 10) * legacy_bonus)
                current_generation += 1
                show_heir_choice = True

            # Heir choice
            if show_heir_choice:
                if pygame.Rect(50, 400, 280, 50).collidepoint(mx, my):
                    heir_trait = "Scientist"
                    show_heir_choice = False
                if pygame.Rect(370, 400, 280, 50).collidepoint(mx, my):
                    heir_trait = "Marketer"
                    show_heir_choice = False
                if pygame.Rect(690, 400, 280, 50).collidepoint(mx, my):
                    heir_trait = "Traditionalist"
                    show_heir_choice = False

            # Event choices
            if current_event:
                if pygame.Rect(300, 380, 180, 50).collidepoint(mx, my):
                    choice = current_event["choices"][0]
                    if choice["effect"] == "damage_all":
                        for row in grid:
                            for plot in row:
                                if plot.varietal:
                                    plot.health = max(0, plot.health + choice["value"])
                    elif choice["effect"] == "cost_research":
                        research_points = max(0, research_points - choice["value"])
                    elif choice["effect"] == "legacy_bonus":
                        legacy_score += choice["value"]
                    current_event = None
                if pygame.Rect(500, 380, 180, 50).collidepoint(mx, my):
                    choice = current_event["choices"][1]
                    if choice["effect"] == "damage_all":
                        for row in grid:
                            for plot in row:
                                if plot.varietal:
                                    plot.health = max(0, plot.health + choice["value"])
                    elif choice["effect"] == "cost_research":
                        research_points = max(0, research_points - choice["value"])
                    elif choice["effect"] == "legacy_bonus":
                        legacy_score += choice["value"]
                    current_event = None

    screen.fill(BROWN)

    if victory:
        screen.blit(big_font.render("VICTORY!", True, VICTORY_COLOR), (320, 220))
        screen.blit(font.render(f"Final Legacy: {legacy_score}  |  Final Cash: ${money}", True, BLACK), (280, 320))
        pygame.draw.rect(screen, BUTTON_COLOR, (400, 500, 200, 60))
        screen.blit(font.render("New Game", True, (255,255,255)), (440, 515))
    else:
        # Realistic vineyard grid
        for y in range(5):
            for x in range(5):
                rect = pygame.Rect(x * 120 + 50, y * 120 + 50, 100, 100)
                draw_vineyard_plot(screen, rect, grid[y][x])

        # Main buttons
        pygame.draw.rect(screen, BUTTON_COLOR, (700, 50, 200, 60))
        screen.blit(font.render("HARVEST", True, (255,255,255)), (730, 65))

        pygame.draw.rect(screen, TECH_COLOR, (700, 130, 200, 60))
        screen.blit(small_font.render("RESEARCH ($300)", True, (255,255,255)), (720, 145))
        screen.blit(small_font.render(f"Points: {research_points}", True, BLACK), (730, 180))

        pygame.draw.rect(screen, GENERATION_COLOR, (700, 210, 200, 60))
        screen.blit(small_font.render("END GEN", True, (255,255,255)), (730, 225))

        # Heir choice
        if show_heir_choice:
            pygame.draw.rect(screen, HEIR_COLOR, (50, 400, 280, 50))
            screen.blit(small_font.render("Scientist", True, (255,255,255)), (120, 415))
            pygame.draw.rect(screen, HEIR_COLOR, (370, 400, 280, 50))
            screen.blit(small_font.render("Marketer", True, (255,255,255)), (440, 415))
            pygame.draw.rect(screen, HEIR_COLOR, (690, 400, 280, 50))
            screen.blit(small_font.render("Traditionalist", True, (255,255,255)), (740, 415))

        # Event popup
        if current_event:
            pygame.draw.rect(screen, EVENT_COLOR, (200, 250, 600, 220))
            pygame.draw.rect(screen, BLACK, (200, 250, 600, 220), 4)
            screen.blit(font.render(current_event["title"], True, (255,255,255)), (250, 270))
            screen.blit(small_font.render(current_event["desc"], True, (255,255,255)), (250, 320))
            pygame.draw.rect(screen, (100,100,100), (300, 380, 180, 50))
            screen.blit(small_font.render(current_event["choices"][0]["text"], True, (255,255,255)), (330, 395))
            pygame.draw.rect(screen, (100,100,100), (500, 380, 180, 50))
            screen.blit(small_font.render(current_event["choices"][1]["text"], True, (255,255,255)), (520, 395))

        # Variety buttons (moved lower)
        varieties = ["Nebbiolo", "Chardonnay", "Cabernet Sauvignon"]
        for i, var in enumerate(varieties):
            x = 50 + i * 200
            color = SELECTED_COLOR if current_variety == var else BUTTON_COLOR
            pygame.draw.rect(screen, color, (x, 670, 180, 50))
            screen.blit(small_font.render(var, True, (255,255,255)), (x + 20, 685))

        # Money + Market prices
        money_color = (0, 200, 0) if money >= 0 else (200, 0, 0)
        screen.blit(font.render(f"Cash: ${money}", True, money_color), (700, 10))

        market_y = 280
        screen.blit(small_font.render("Current Market:", True, BLACK), (700, market_y))
        market_y += 25
        for var in ["Nebbiolo", "Chardonnay", "Cabernet Sauvignon"]:
            price = current_market_prices.get(var, 0)
            screen.blit(small_font.render(f"{var[:4]}: ${price}", True, BLACK), (700, market_y))
            market_y += 22

        # Status line (moved lower, bottom-left)
        status = small_font.render(f"Selected: {current_variety}  |  Tech: {'ON' if unlocked_tech else 'OFF'}  |  Heir: {heir_trait}  |  Legacy: {legacy_score}", True, BLACK)
        screen.blit(status, (50, 720))

        title = font.render(f"Legacy Vines - Gen {current_generation}  |  Year: {simulator.year}", True, BLACK)
        screen.blit(title, (50, 10))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()