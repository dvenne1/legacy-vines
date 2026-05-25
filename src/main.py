import pygame
import sys
from pathlib import Path

# Fix imports so we can run from root folder (professional habit)
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

# Simple 5x5 vineyard grid
grid = [[Plot(x, y) for x in range(5)] for y in range(5)]

# Season simulator
simulator = SeasonSimulator()

clock = pygame.time.Clock()
running = True
font = pygame.font.SysFont(None, 36)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # MOUSE CLICK - plant vine
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            
            # Check if click is on a grid tile
            for y in range(5):
                for x in range(5):
                    rect = pygame.Rect(x * 120 + 50, y * 120 + 50, 100, 100)
                    if rect.collidepoint(mouse_x, mouse_y):
                        grid[y][x].plant("Nebbiolo")   # default variety for now

            # Check if click is on Harvest button
            button_rect = pygame.Rect(700, 50, 200, 60)
            if button_rect.collidepoint(mouse_x, mouse_y):
                print("\n=== HARVEST STARTED ===")
                simulator.simulate_harvest(grid)
                print("=== HARVEST FINISHED ===\n")

    # Fill background
    screen.fill(BROWN)

    # Draw vineyard grid
    for y in range(5):
        for x in range(5):
            rect = pygame.Rect(x * 120 + 50, y * 120 + 50, 100, 100)
            color = GREEN if grid[y][x].varietal is None else (139, 0, 0)  # red = planted
            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, BLACK, rect, 3)
            
            # Show simple label if planted
            if grid[y][x].varietal:
                label = font.render("V", True, BLACK)
                screen.blit(label, (x * 120 + 80, y * 120 + 70))

    # Harvest button
    button_rect = pygame.Rect(700, 50, 200, 60)
    pygame.draw.rect(screen, BUTTON_COLOR, button_rect)
    button_text = font.render("HARVEST", True, (255, 255, 255))
    screen.blit(button_text, (button_rect.x + 30, button_rect.y + 15))

    # Title + year
    title = font.render(f"Legacy Vines - Generation 1  |  Year: {simulator.year}", True, BLACK)
    screen.blit(title, (50, 10))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
