import pygame
import sys
import random

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
        if self.owner == "human":
            pygame.draw.polygon(surface, (0, 0, 255), [
                (self.x, self.y - 5),
                (self.x - 5, self.y + 5),
                (self.x + 5, self.y + 5)
            ])
        elif self.owner == "ai":
            pygame.draw.rect(surface, (255, 0, 0), (self.x - 5, self.y - 5, 10, 10))
        else:
            pygame.draw.circle(surface, (0, 0, 0), (self.x, self.y), 2)

def generate_stars(star_count=100, min_distance=10, max_attempts=1000):
    stars = []
    attempts = 0
    while len(stars) < star_count and attempts < max_attempts:
        x = random.randint(20, width - 20)  # Ensure stars are not too close to the border
        y = random.randint(20, height - 20)
        if all(abs(x - star.x) > min_distance and abs(y - star.y) > min_distance for star in stars):
            ships_per_turn = random.randint(1, 6)
            stars.append(Star(x, y, ships_per_turn))
        attempts += 1
    return stars

def draw_stars(surface, stars):
    for star in stars:
        star.draw(surface)

def display_info(surface, star, position):
    font = pygame.font.Font(None, 36)
    if star.owner == "human":
        text = f"Owner: {star.owner}, Ships: {star.total_ships}, Ships/Turn: {star.ships_per_turn}"
    else:
        text = f"Owner: {star.owner}"
    text_surface = font.render(text, True, (0, 0, 0))
    if position == "left":
        surface.blit(text_surface, (10, 10))
    else:
        surface.blit(text_surface, (width - text_surface.get_width() - 10, 10))

def draw_players(surface, human_pos, ai_pos):
    # Draw human player as a smaller triangle
    pygame.draw.polygon(surface, (0, 0, 255), [
        (human_pos[0], human_pos[1] - 5),
        (human_pos[0] - 5, human_pos[1] + 5),
        (human_pos[0] + 5, human_pos[1] + 5)
    ])
    # Draw AI player as a smaller square
    pygame.draw.rect(surface, (255, 0, 0), (*ai_pos, 10, 10))

# Generate stars once, ensuring they don't overlap with each other
stars = generate_stars(star_count=100, min_distance=5)

# Randomly select one star for the human and one for the AI
human_star = random.choice(stars)
human_star.owner = "human"
human_star.ships_per_turn = 10
human_star.total_ships = 10

ai_star = random.choice([star for star in stars if star != human_star])
ai_star.owner = "ai"
ai_star.ships_per_turn = 10
ai_star.total_ships = 10

# Main game loop
selected_star = None
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            if selected_star:
                selected_star = None  # Close the information window if already open
            else:
                for star in stars:
                    if abs(star.x - mouse_x) < 5 and abs(star.y - mouse_y) < 5:
                        selected_star = star
                        break

    # Fill the screen with a white color (RGB)
    window.fill((255, 255, 255))

    # Draw stars on the screen
    draw_stars(window, stars)

    # Display information if a star is selected
    if selected_star:
        position = "left" if selected_star.x < width // 2 else "right"
        display_info(window, selected_star, position)

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)