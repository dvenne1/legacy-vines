import pygame
import sys
from pathlib import Path

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

grid = [[Plot(x, y) for x in range(5)] for y in range(5)]
simulator = SeasonSimulator()

current_variety = "Nebbiolo"
research_points = 0
unlocked_tech = False
current_generation = 1
legacy_score = 0

clock = pygame.time.Clock()
running = True
font = pygame.font.SysFont(None, 36)
small_font = pygame.font.SysFont(None, 24)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()

            # Plant on grid
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
                simulator.simulate_harvest(grid, tech_bonus)
                research_points += 1
                print(f"Research points earned: {research_points}")
                print("=== HARVEST FINISHED ===\n")

            # RESEARCH
            if pygame.Rect(700, 130, 200, 60).collidepoint(mx, my) and research_points > 0:
                unlocked_tech = True
                research_points -= 1
                print("=== RESEARCHED: Improved Rootstock (+20% yield) ===")

            # END GENERATION (new!)
            if pygame.Rect(700, 210, 200, 60).collidepoint(mx, my):
                legacy_score += 100 + (simulator.year - 1850) * 10   # simple legacy formula
                current_generation += 1
                print(f"\n=== GENERATION {current_generation-1} ENDED ===")
                print(f"Legacy score increased! Total legacy: {legacy_score}")
                print("New generation begins...\n")
                # For now we keep the vines (they carry over as "old vines")
                # Later we can add heir trait choices

    # Draw
    screen.fill(BROWN)

    # Grid
    for y in range(5):
        for x in range(5):
            rect = pygame.Rect(x * 120 + 50, y * 120 + 50, 100, 100)
            color = GREEN if grid[y][x].varietal is None else (139, 0, 0)
            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, BLACK, rect, 3)
            if grid[y][x].varietal:
                label = font.render("V", True, BLACK)
                screen.blit(label, (x * 120 + 80, y * 120 + 70))

    # Harvest button
    pygame.draw.rect(screen, BUTTON_COLOR, (700, 50, 200, 60))
    screen.blit(font.render("HARVEST", True, (255,255,255)), (730, 65))

    # Research button
    pygame.draw.rect(screen, TECH_COLOR, (700, 130, 200, 60))
    screen.blit(small_font.render("RESEARCH", True, (255,255,255)), (730, 145))
    screen.blit(small_font.render(f"Points: {research_points}", True, BLACK), (730, 180))

    # End Generation button (purple)
    pygame.draw.rect(screen, GENERATION_COLOR, (700, 210, 200, 60))
    screen.blit(small_font.render("END GENERATION", True, (255,255,255)), (720, 225))

    # Variety buttons
    varieties = ["Nebbiolo", "Chardonnay", "Cabernet Sauvignon"]
    for i, var in enumerate(varieties):
        x = 50 + i * 200
        color = SELECTED_COLOR if current_variety == var else BUTTON_COLOR
        pygame.draw.rect(screen, color, (x, 620, 180, 50))
        screen.blit(small_font.render(var, True, (255,255,255)), (x + 20, 635))

    # Status
    title = font.render(f"Legacy Vines - Gen {current_generation}  |  Year: {simulator.year}", True, BLACK)
    screen.blit(title, (50, 10))
    status = small_font.render(f"Selected: {current_variety}  |  Tech: {'ON (+20%)' if unlocked_tech else 'OFF'}  |  Legacy: {legacy_score}", True, BLACK)
    screen.blit(status, (50, 580))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()