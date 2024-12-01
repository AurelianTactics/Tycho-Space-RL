import random
import pygame
import string

# Contents of /tycho-space-rl/tycho-space-rl/src/standalone_game/game_logic.py

# This file contains the core game logic for the standalone game, including the rules and mechanics of Tycho Space RL.

class Star:
    def __init__(self, index, x, y, owner=-1, total_ships=0, min_ships_per_turn=1, max_ships_per_turn=6, name=None):
        self.index = index
        self.x = x
        self.y = y
        self.owner = owner
        self.total_ships = total_ships
        self.ships_per_turn = random.randint(min(min_ships_per_turn, max_ships_per_turn), max(min_ships_per_turn, max_ships_per_turn))
        self.name = name or self.generate_name()

    def generate_name(self):
        vowels = "aeiou"
        consonants = "".join(set(string.ascii_lowercase) - set(vowels))
        name = []
        length = random.randint(3, 7)
        for i in range(length):
            if i % 2 == 0:
                name.append(random.choice(consonants))
            else:
                name.append(random.choice(vowels))
        return ''.join(name)

class StarMap:
    def __init__(self, map_width=10, map_height=10, seed=None, min_distance=5, star_probability=0.1, 
                 min_ships_per_turn=1, max_ships_per_turn=6, max_stars=None, edge_buffer=1):
        self.width = max(10, min(map_width, 1000))
        self.height = max(10, min(map_height, 1000))
        self.seed = seed
        self.min_distance = min_distance
        self.star_probability = star_probability
        self.min_ships_per_turn = min_ships_per_turn
        self.max_ships_per_turn = max_ships_per_turn
        self.max_stars = max_stars
        self.edge_buffer = edge_buffer
        self.map, self.stars = self.generate_star_map()
        self.total_stars = self.calculate_total_stars()

    def generate_star_map(self):
        random.seed(self.seed)
        star_map = [[0 for _ in range(self.width)] for _ in range(self.height)]
        stars = []

        for y in range(self.edge_buffer, self.height - self.edge_buffer):
            for x in range(self.edge_buffer, self.width - self.edge_buffer):
                if self.can_place_star(x, y, stars):
                    if random.random() < self.star_probability:
                        star = Star(len(stars), x, y, min_ships_per_turn=self.min_ships_per_turn,
                                        max_ships_per_turn=self.max_ships_per_turn)
                        star_map[y][x] = star
                        stars.append(star)

        if self.max_stars is not None and len(stars) > self.max_stars:
            stars = random.sample(stars, self.max_stars)
            star_map = [[0 for _ in range(self.width)] for _ in range(self.height)]
            for star in stars:
                star_map[star.y][star.x] = star

        return star_map, stars

    def can_place_star(self, x, y, stars):
        for star in stars:
            if abs(star.x - x) < self.min_distance and abs(star.y - y) < self.min_distance:
                return False
        return True

    def calculate_total_stars(self):
        return sum(1 for row in self.map for cell in row if isinstance(cell, Star))

class Game:
    def __init__(self, map_width=10, map_height=10, seed=None, min_distance=5, star_probability=0.1,
                 min_ships_per_turn=1, max_ships_per_turn=6, max_stars=None, num_players=2):
        self.players = []
        self.current_turn = 0
        self.star_map = StarMap(map_width=map_width, map_height=map_height, seed=seed, min_distance=min_distance,
                                star_probability=star_probability,
                                min_ships_per_turn=min_ships_per_turn, max_ships_per_turn=max_ships_per_turn,
                                max_stars=max_stars)
        self.num_players = num_players
        self.player_colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0)]  # Add more colors if needed
        self.player_shapes = ["circle", "square", "triangle", "hexagon"]  # Add more shapes if needed
        self.generate_players()

    def generate_players(self):
        for i in range(self.num_players):
            player_home_star = random.choice([star for star in self.star_map.stars if star.owner == -1])
            player_home_star.owner = i
            player_home_star.total_ships = 10
            player_home_star.ships_per_turn = 10
            player_home_star.color = self.player_colors[i % len(self.player_colors)]
            player_home_star.shape = self.player_shapes[i % len(self.player_shapes)]
            self.players.append(player_home_star)

    def capture_star(self):
        # to do fix this
        pass


    def end_turn(self):
        # to do fix this
        pass

    def check_winner(self):
        # to do fix this
        pass
        # total_stars = self.star_map.total_stars
        # for player, star_count in self.stars.items():
        #     if star_count >= total_stars:
        #         return player
        # return None

    def total_stars(self):
        return len(self.star_map.stars)

    def reset_game(self):
        # to do: generate a new star map
        self.current_turn = 0

def show_star_info(screen, star):
    font = pygame.font.Font(None, 36)
    info_text = [
        f"Name: {star.name}",
        f"Owner: {star.owner}",
        f"Total Ships: {star.total_ships}",
        f"Ships per Turn: {star.ships_per_turn}",
        f"Position: ({star.x}, {star.y})"
    ]
    info_surface = pygame.Surface((400, 200))
    info_surface.fill((255, 255, 255))
    for i, text in enumerate(info_text):
        text_surface = font.render(text, True, (0, 0, 0))
        info_surface.blit(text_surface, (10, 10 + i * 30))
    screen.blit(info_surface, (200, 200))
    pygame.display.flip()

def draw_star_map(star_map, screen):
    BLACK = (0, 0, 0)
    SOFT_WHITE = (200, 200, 200)
    screen.fill(BLACK)
    cell_width = screen.get_width() // star_map.width
    cell_height = screen.get_height() // star_map.height

    for y in range(star_map.height):
        for x in range(star_map.width):
            if isinstance(star_map.map[y][x], Star):
                star = star_map.map[y][x]
                if star.owner == -1:
                    pygame.draw.circle(screen, SOFT_WHITE, (x * cell_width + cell_width // 2, y * cell_height + cell_height // 2), min(cell_width, cell_height) // 4)
                else:
                    color = star.color
                    shape = star.shape
                    if shape == "circle":
                        pygame.draw.circle(screen, color, (x * cell_width + cell_width, y * cell_height + cell_height), min(cell_width, cell_height) // 2)
                    elif shape == "square":
                        pygame.draw.rect(screen, color, (x * cell_width // 2, y * cell_width // 2, cell_width // 2, cell_width // 2))
                    # Add more shapes as needed

    pygame.display.flip()

# Additional game logic methods can be added as needed.