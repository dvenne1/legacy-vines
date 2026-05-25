import pygame
import sys
from pathlib import Path

# Fix imports so we can run from root folder
sys.path.insert(0, str(Path(__file__).parent))

from plot import Plot
from season import SeasonSimulator

# Initialize Pygame
pygame.init()

# Screen settings
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Legacy Vines - Prototype")

# Colors
BLACK = (0, 0, 0)
GREEN = (34, 139, 34)
BROWN = (139, 69, 19)
BUTTON_COLOR = (200, 0, 0)
SELECTED_COLOR = (0, 200, 0)

# Simple 5x5 vineyard grid
grid = [[Plot(x, y) for x in range(5)] for y in range(5)]

# Season simulator
simulator = SeasonSimulator()

# Current variety the player has selected
current_variety = "Nebbiolo"

clock = pygame.time.Clock()
running = True
font = pygame.font.SysFont(None, 36)
small_font = pygame.font.SysFont(None, 24)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()

            # PLANT on grid
            for y in range(5):
                for x in range(5):
                    rect = pygame.Rect(x * 120 + 50, y * 120 + 50, 100, 100)
                    if rect.collidepoint(mouse_x, mouse_y):
                        grid[y][x].plant(current_variety)

            # VARIETY BUTTONS
            if pygame.Rect(50, 620, 180, 50).collidepoint(mouse_x, mouse_y):
                current_variety = "Nebbiolo"
            if pygame.Rect(250, 620, 180, 50).collidepoint(mouse_x, mouse_y):
                current_variety = "Chardonnay"
            if pygame.Rect(450, 620, 180, 50).collidepoint(mouse_x, mouse_y):
                current_variety = "Cabernet Sauvignon"

            # HARVEST
            button_rect = pygame.Rect(700, 50, 200, 60)
            if button_rect.collidepoint(mouse_x, mouse_y):
                print("\n=== HARVEST STARTED ===")
                simulator.simulate_harvest(grid)
                print("=== HARVEST FINISHED ===\n")

    # Draw everything
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
    button_rect = pygame.Rect(700, 50, 200, 60)
    pygame.draw.rect(screen, BUTTON_COLOR, button_rect)
    button_text = font.render("HARVEST", True, (255, 255, 255))
    screen.blit(button_text, (button_rect.x + 30, button_rect.y + 15))

    # Variety buttons
    varieties = ["Nebbiolo", "Chardonnay", "Cabernet Sauvignon"]
    for i, var in enumerate(varieties):
        x = 50 + i * 200
        color = SELECTED_COLOR if current_variety == var else BUTTON_COLOR
        btn_rect = pygame.Rect(x, 620, 180, 50)
        pygame.draw.rect(screen, color, btn_rect)
        text = small_font.render(var, True, (255, 255, 255))
        screen.blit(text, (x + 20, 635))

    # Title
    title = font.render(f"Legacy Vines - Generation 1  |  Year: {simulator.year}", True, BLACK)
    screen.blit(title, (50, 10))
    status = small_font.render(f"Selected: {current_variety}", True, BLACK)
    screen.blit(status, (50, 580))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()