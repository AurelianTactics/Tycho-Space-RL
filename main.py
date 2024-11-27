import pygame
import sys
import random

#print("Hello World!")
# Initialize pygame
pygame.init()

# Set up display
width, height = 800, 600
window = pygame.display.set_mode((width, height))
pygame.display.set_caption('Simple Game')

# Set up the clock for a decent framerate
clock = pygame.time.Clock()

class Star:
    def __init__(self, x, y, ships_per_turn, total_ships=0, owner="unowned"):
        self.x = x
        self.y = y
        self.ships_per_turn = ships_per_turn
        self.total_ships = total_ships
        self.owner = owner

    def draw(self, surface):
        pygame.draw.circle(surface, (0, 0, 0), (self.x, self.y), 2)

def generate_stars(star_count=100, exclude_positions=[]):
    stars = []
    while len(stars) < star_count:
        x = random.randint(0, width)
        y = random.randint(0, height)
        if all(abs(x - ex[0]) > 50 and abs(y - ex[1]) > 50 for ex in exclude_positions):
            ships_per_turn = random.randint(1, 6)
            stars.append(Star(x, y, ships_per_turn))
    return stars

def draw_stars(surface, stars):
    for star in stars:
        star.draw(surface)

# Randomize player positions
human_pos = (random.randint(50, width - 50), random.randint(50, height - 50))
ai_pos = (random.randint(50, width - 50), random.randint(50, height - 50))

def draw_players(surface, human_pos, ai_pos):
    # Draw human player as a smaller triangle
    pygame.draw.polygon(surface, (0, 0, 255), [
        (human_pos[0], human_pos[1] - 5),
        (human_pos[0] - 5, human_pos[1] + 5),
        (human_pos[0] + 5, human_pos[1] + 5)
    ])
    # Draw AI player as a smaller square
    pygame.draw.rect(surface, (255, 0, 0), (*ai_pos, 10, 10))

# Generate stars once, ensuring they don't overlap with players
stars = generate_stars(star_count=98, exclude_positions=[human_pos, ai_pos])
stars.append(Star(human_pos[0], human_pos[1], ships_per_turn=10, total_ships=10, owner="human"))
stars.append(Star(ai_pos[0], ai_pos[1], ships_per_turn=10, total_ships=10, owner="ai"))

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Fill the screen with a white color (RGB)
    window.fill((255, 255, 255))

    # Draw stars on the screen
    draw_stars(window, stars)

    # Draw players on the screen
    draw_players(window, human_pos, ai_pos)

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)