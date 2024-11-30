import random
import pygame

# Contents of /tycho-space-rl/tycho-space-rl/src/standalone_game/game_logic.py

# This file contains the core game logic for the standalone game, including the rules and mechanics of Tycho Space RL.

class Star:
    def __init__(self, index, x, y, owner=-1, total_ships=0, min_ships_per_turn=1, max_ships_per_turn=6):
        self.index = index
        self.x = x
        self.y = y
        self.owner = owner
        self.total_ships = total_ships
        self.ships_per_turn = random.randint(min_ships_per_turn, max_ships_per_turn)

class StarMap:
    def __init__(self, width=10, height=10, seed=None, min_distance=0, star_probability=0.1, min_ships_per_turn=1, max_ships_per_turn=6):
        self.width = max(10, min(width, 1000))
        self.height = max(10, min(height, 1000))
        self.seed = seed
        self.min_distance = min_distance
        self.star_probability = star_probability
        self.min_ships_per_turn = min_ships_per_turn
        self.max_ships_per_turn = max_ships_per_turn
        self.map = self.generate_star_map()
        self.total_stars = self.calculate_total_stars()

    def generate_star_map(self):
        random.seed(self.seed)
        star_map = [[0 for _ in range(self.width)] for _ in range(self.height)]
        stars = []

        for y in range(self.height):
            for x in range(self.width):
                if self.can_place_star(x, y, stars):
                    if random.random() < self.star_probability:
                        star = Star(len(stars), x, y, min_ships_per_turn=self.min_ships_per_turn, max_ships_per_turn=self.max_ships_per_turn)
                        star_map[y][x] = star
                        stars.append(star)

        return star_map

    def can_place_star(self, x, y, stars):
        for star in stars:
            if abs(star.x - x) < self.min_distance and abs(star.y - y) < self.min_distance:
                return False
        return True

    def calculate_total_stars(self):
        return sum(1 for row in self.map for cell in row if isinstance(cell, Star))

class Game:
    def __init__(self, map_width=10, map_height=10, seed=None, min_distance=0, star_probability=0.1):
        self.players = []
        self.current_turn = 0
        self.stars = {}
        self.star_map = StarMap(map_width, map_height, seed, min_distance, star_probability)
    
    def add_player(self, player):
        self.players.append(player)
        self.stars[player] = 1  # Each player starts with one star

    def capture_star(self, player):
        if player in self.players:
            self.stars[player] += 1

    def end_turn(self):
        self.current_turn = (self.current_turn + 1) % len(self.players)

    def check_winner(self):
        total_stars = self.star_map.total_stars
        for player, star_count in self.stars.items():
            if star_count >= total_stars:
                return player
        return None

    def total_stars(self):
        return sum(self.stars.values())

    def reset_game(self):
        self.stars = {player: 1 for player in self.players}
        self.current_turn = 0

def draw_star_map(star_map, screen):
    BLACK = (0, 0, 0)
    SOFT_WHITE = (200, 200, 200)
    screen.fill(BLACK)
    cell_width = screen.get_width() // star_map.width
    cell_height = screen.get_height() // star_map.height

    for y in range(star_map.height):
        for x in range(star_map.width):
            if isinstance(star_map.map[y][x], Star):
                pygame.draw.circle(screen, SOFT_WHITE, (x * cell_width + cell_width // 2, y * cell_height + cell_height // 2), min(cell_width, cell_height) // 4)

    pygame.display.flip()

# Additional game logic methods can be added as needed.