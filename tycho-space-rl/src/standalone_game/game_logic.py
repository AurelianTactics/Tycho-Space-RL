import random
import pygame
import string
import math

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

    def distance_to(self, other_star):
        return math.sqrt((self.x - other_star.x) ** 2 + (self.y - other_star.y) ** 2)

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
                 min_ships_per_turn=1, max_ships_per_turn=6, max_stars=None, num_players=2,
                 max_turns=1000, victory_percentage=0.9, distance_ships_travel_per_turn=5):
        self.players = []
        self.current_turn = 0
        self.turn = 0
        self.star_map = StarMap(map_width=map_width, map_height=map_height, seed=seed, min_distance=min_distance,
                                star_probability=star_probability,
                                min_ships_per_turn=min_ships_per_turn, max_ships_per_turn=max_ships_per_turn,
                                max_stars=max_stars)
        self.num_players = num_players
        self.max_turns = max_turns
        self.victory_percentage = victory_percentage
        self.distance_ships_travel_per_turn = distance_ships_travel_per_turn
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

    def increment_turn(self):
        self.turn += 1

    def check_victory_conditions(self):
        player_star_counts = {i: 0 for i in range(self.num_players)}
        for star in self.star_map.stars:
            if star.owner != -1:
                player_star_counts[star.owner] += 1

        # Check if only one player owns a star
        active_players = [player for player, count in player_star_counts.items() if count > 0]
        if len(active_players) == 1:
            return active_players[0]

        # Check if a player owns >= 90% of the stars
        total_stars = len(self.star_map.stars)
        for player, count in player_star_counts.items():
            if count / total_stars >= self.victory_percentage:
                return player

        # Check if the game reaches the maximum number of turns
        if self.turn >= self.max_turns:
            max_stars = max(player_star_counts.values())
            winners = [player for player, count in player_star_counts.items() if count == max_stars]
            if len(winners) == 1:
                return winners[0]
            else:
                return -1  # Tie, no winner

        return None  # No winner yet

    def calculate_travel_turns(self, star1, star2):
        distance = star1.distance_to(star2)
        return math.ceil(distance / self.distance_ships_travel_per_turn)

    def capture_star(self):
        # to do fix this
        pass

    def end_turn(self):
        self.increment_turn()
        winner = self.check_victory_conditions()
        if winner is not None:
            print(f"Player {winner} wins!")
            return winner
        # to do fix this

    def check_winner(self):
        return self.check_victory_conditions()

    def total_stars(self):
        return len(self.star_map.stars)

    def reset_game(self):
        # to do: generate a new star map
        self.current_turn = 0
        self.turn = 0

    def step(self, action):
        # Implement the logic for a single step in the game
        # to do: implement the logic for a single step in the game

        winner = self.check_victory_conditions()

        obs = self.get_observation()
        reward = self.get_reward(winner)
        terminated = self.get_is_terminated(winner)
        truncated = self.get_is_truncated(winner)
        info = self.get_info()

        return obs, reward, terminated, truncated, info

    def get_observation(self):
        # Return the current observation of the game state
        pass

    def get_reward(self, winner):
        # Return the reward for the current state
        # to do: logic for multiple players
        if winner is None or winner == -1:
            reward = 0.
        elif winner == 0:
            reward = 1.
        elif winner == 1:
            reward = -1.

        return reward

    def get_is_terminated(self, winner):
        # Return whether the game has terminated

        if winner is not None:
            is_terminated = True
        else:
            is_terminated = False

        return is_terminated

    def get_is_truncated(self, winner):
        # Return whether the game has been truncated
        return False

    def get_info(self):
        # Return additional information about the current state
        return {}

def show_star_info(screen, star, offset=(0, 0)):
    font = pygame.font.Font(None, 36)
    info_text = [
        f"Name: {star.name}",
        f"Owner: {star.owner}",
        f"Total Ships: {star.total_ships}",
        f"Ships per Turn: {star.ships_per_turn}",
        f"Position: ({star.x}, {star.y})"
    ]
    for i, text in enumerate(info_text):
        text_surface = font.render(text, True, (0, 0, 0))
        screen.blit(text_surface, (offset[0], offset[1] + i * 30))

def draw_star_map(star_map, screen, offset_x=0):
    BLACK = (0, 0, 0)
    SOFT_WHITE = (200, 200, 200)
    screen.fill(BLACK)
    cell_width = (screen.get_width() - offset_x) // star_map.width
    cell_height = screen.get_height() // star_map.height

    for y in range(star_map.height):
        for x in range(star_map.width):
            if isinstance(star_map.map[y][x], Star):
                star = star_map.map[y][x]
                if star.owner == -1:
                    pygame.draw.circle(screen, SOFT_WHITE, (x * cell_width + cell_width // 2 + offset_x, y * cell_height + cell_height // 2), min(cell_width, cell_height) // 4)
                else:
                    color = star.color
                    shape = star.shape
                    if shape == "circle":
                        pygame.draw.circle(screen, color, (x * cell_width + cell_width // 2 + offset_x, y * cell_height + cell_height // 2), min(cell_width, cell_height) // 4)
                    elif shape == "square":
                        pygame.draw.rect(screen, color, (x * cell_width + offset_x, y * cell_height, cell_width, cell_height))
                    # Add more shapes as needed

    pygame.display.flip()

# Additional game logic methods can be added as needed.