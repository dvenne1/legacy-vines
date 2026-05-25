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

grid = [[Plot(x, y) for x in range(5)] for y in range(5)]
simulator = SeasonSimulator()

current_variety = "Nebbiolo"
research_points = 0
unlocked_tech = False
current_generation = 1
legacy_score = 0
heir_trait = "None"
show_heir_choice = False
current_event = None

# Load events from JSON (data-driven)
def load_events():
    path = Path(__file__).parent.parent / "data" / "events.json"
    with open(path) as f:
        return json.load(f)

events_list = load_events()

clock = pygame.time.Clock()
running = True
font = pygame.font.SysFont(None, 36)
small_font = pygame.font.SysFont(None, 20)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()

            # Plant
            for y in range(5):
                for x in range(5):
                    rect = pygame.Rect(x * 120 + 50, y * 120 + 50, 100, 100)
                    if rect.collidepoint(mx, my):
                        grid[y][x].plant(current_variety)

            # Variety buttons
            if pygame.Rect(50, 620, 180, 50).collidepoint(mx, my):
                current_variety = "Nebbiolo"
            if pygame.Rect(250, 620, 180, 50).collidepoint(mx, my):
                current_variety = "Chardonnay"
            if pygame.Rect(450, 620, 180, 50).collidepoint(mx, my):
                current_variety = "Cabernet Sauvignon"

            # HARVEST
            if pygame.Rect(700, 50, 200, 60).collidepoint(mx, my):
                print("\n=== HARVEST STARTED ===")
                tech_bonus = 1.2 if unlocked_tech else 1.0
                aging_multiplier = 1.15 if heir_trait == "Traditionalist" else 1.0
                extra_research = 1 if heir_trait == "Scientist" else 0

                simulator.simulate_harvest(grid, tech_bonus, aging_multiplier)
                research_points += 1 + extra_research

                # Random event (25% chance)
                if random.random() < 0.25:
                    current_event = random.choice(events_list)
                    print(f"EVENT: {current_event['title']}")

                print("=== HARVEST FINISHED ===\n")

            # RESEARCH
            if pygame.Rect(700, 130, 200, 60).collidepoint(mx, my) and research_points > 0:
                unlocked_tech = True
                research_points -= 1
                print("=== RESEARCHED: Improved Rootstock (+20% yield) ===")

            # END GENERATION
            if pygame.Rect(700, 210, 200, 60).collidepoint(mx, my) and not show_heir_choice:
                legacy_bonus = 1.1 if heir_trait == "Marketer" else 1.0
                legacy_score += int((100 + (simulator.year - 1850) * 10) * legacy_bonus)
                current_generation += 1
                show_heir_choice = True
                print(f"\n=== GENERATION {current_generation-1} ENDED ===")
                print(f"Legacy score: {legacy_score}\nChoose your heir:\n")

            # Heir choice
            if show_heir_choice:
                if pygame.Rect(50, 400, 280, 50).collidepoint(mx, my):
                    heir_trait = "Scientist"
                    show_heir_choice = False
                    print("Heir: Scientist (+1 research per harvest)")
                if pygame.Rect(370, 400, 280, 50).collidepoint(mx, my):
                    heir_trait = "Marketer"
                    show_heir_choice = False
                    print("Heir: Marketer (+10% legacy)")
                if pygame.Rect(690, 400, 280, 50).collidepoint(mx, my):
                    heir_trait = "Traditionalist"
                    show_heir_choice = False
                    print("Heir: Traditionalist (+15% aging bonus)")

            # Event choice handling (now works for any event)
            if current_event:
                # Left button
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

                # Right button
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

    # Grid
    for y in range(5):
        for x in range(5):
            rect = pygame.Rect(x * 120 + 50, y * 120 + 50, 100, 100)
            color = GREEN if grid[y][x].varietal is None else (139, 0, 0)
            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, BLACK, rect, 3)

            if grid[y][x].varietal:
                varieties = Plot.load_varieties()
                data = varieties[grid[y][x].varietal]
                short_name = data.get("short_name", grid[y][x].varietal[:4])
                var_text = small_font.render(short_name, True, BLACK)
                screen.blit(var_text, (x * 120 + 58, y * 120 + 58))
                age_text = small_font.render(f"Age:{grid[y][x].age}", True, BLACK)
                screen.blit(age_text, (x * 120 + 58, y * 120 + 78))

    # Main buttons
    pygame.draw.rect(screen, BUTTON_COLOR, (700, 50, 200, 60))
    screen.blit(font.render("HARVEST", True, (255,255,255)), (730, 65))

    pygame.draw.rect(screen, TECH_COLOR, (700, 130, 200, 60))
    screen.blit(small_font.render("RESEARCH", True, (255,255,255)), (730, 145))
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

    # Event popup (now supports any event from JSON)
    if current_event:
        pygame.draw.rect(screen, EVENT_COLOR, (200, 250, 600, 220))
        pygame.draw.rect(screen, BLACK, (200, 250, 600, 220), 4)
        screen.blit(font.render(current_event["title"], True, (255,255,255)), (250, 270))
        screen.blit(small_font.render(current_event["desc"], True, (255,255,255)), (250, 320))

        # Left button
        pygame.draw.rect(screen, (100,100,100), (300, 380, 180, 50))
        screen.blit(small_font.render(current_event["choices"][0]["text"], True, (255,255,255)), (330, 395))

        # Right button
        pygame.draw.rect(screen, (100,100,100), (500, 380, 180, 50))
        screen.blit(small_font.render(current_event["choices"][1]["text"], True, (255,255,255)), (520, 395))

    # Variety buttons
    varieties = ["Nebbiolo", "Chardonnay", "Cabernet Sauvignon"]
    for i, var in enumerate(varieties):
        x = 50 + i * 200
        color = SELECTED_COLOR if current_variety == var else BUTTON_COLOR
        pygame.draw.rect(screen, color, (x, 620, 180, 50))
        screen.blit(small_font.render(var, True, (255,255,255)), (x + 20, 635))

    title = font.render(f"Legacy Vines - Gen {current_generation}  |  Year: {simulator.year}", True, BLACK)
    screen.blit(title, (50, 10))
    status = small_font.render(f"Selected: {current_variety}  |  Tech: {'ON' if unlocked_tech else 'OFF'}  |  Heir: {heir_trait}  |  Legacy: {legacy_score}", True, BLACK)
    screen.blit(status, (50, 580))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()