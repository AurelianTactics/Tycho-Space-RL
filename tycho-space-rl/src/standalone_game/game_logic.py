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

class TychoSpaceGame:
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
        self.ships_in_transit = []
        self.logs = []
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

    def add_ships_in_transit(self, ship_owner, number_of_ships, star_from, star_to):
        turns_to_reach_star = self.calculate_travel_turns(star_from, star_to)
        exact_turns_to_reach_stars = star_from.distance_to(star_to) / self.distance_ships_travel_per_turn
        self.ships_in_transit.append({
            "turns_to_reach_star": turns_to_reach_star,
            "exact_turns_to_reach_stars": exact_turns_to_reach_stars,
            "ship_owner": ship_owner,
            "number_of_ships": number_of_ships,
            "star_from": star_from.index,
            "star_to": star_to.index
        })

    def update_ships_in_transit(self):
        for ship in self.ships_in_transit[:]:
            ship["turns_to_reach_star"] -= 1
            if ship["turns_to_reach_star"] <= 0:
                self.star_battle(ship)
                self.ships_in_transit.remove(ship)

    def star_battle(self, ships_in_transit):
        star_to = self.star_map.stars[ships_in_transit["star_to"]]
        if star_to.owner == ships_in_transit["ship_owner"]:
            star_to.total_ships += ships_in_transit["number_of_ships"]
            self.logs.append(f"Reinforcement: Player {ships_in_transit['ship_owner']} sent {ships_in_transit['number_of_ships']} ships to star {star_to.index}.")
        else:
            if ships_in_transit["number_of_ships"] > star_to.total_ships:
                star_to.total_ships = ships_in_transit["number_of_ships"] - star_to.total_ships
                star_to.owner = ships_in_transit["ship_owner"]
                self.logs.append(f"Battle: Player {ships_in_transit['ship_owner']} won the battle at star {star_to.index} with {star_to.total_ships} ships remaining.")
            else:
                star_to.total_ships -= ships_in_transit["number_of_ships"]
                self.logs.append(f"Battle: Player {star_to.owner} defended star {star_to.index} with {star_to.total_ships} ships remaining.")

    def capture_star(self):
        # to do maybe implement this in star_battle
        # could do things like determine victory conditions and other thigns here
        pass

    def end_turn(self):
        self.logs.append(f"Turn {self.turn} Ended")
        self.increment_turn()
        self.update_ships_in_transit()
        winner = self.check_victory_conditions()
        if winner is not None:
            self.logs.append(f"Player {winner} wins! Victory condition met.")
            print(f"Player {winner} wins!")
            return winner
        self.increment_star_ships()

    def increment_star_ships(self):
        for star in self.star_map.stars:
            star.total_ships += star.ships_per_turn

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
    font = pygame.font.Font(None, 24)  # Smaller font
    owner_symbols = {-1: "☆", 0: "①", 1: "②", 2: "③", 3: "④"}  # Symbols for different owners
    info_text = [
        f"{star.name} {owner_symbols.get(star.owner, '?')}",
        f"Ships: {star.total_ships} (+{star.ships_per_turn}/turn)"
    ]
    for i, text in enumerate(info_text):
        text_surface = font.render(text, True, (0, 0, 0))
        screen.blit(text_surface, (offset[0], offset[1] + i * 20))

def draw_star_map(star_map, screen, offset_x=0, selected_star=None, target_star=None):
    BLACK = (0, 0, 0)
    SOFT_WHITE = (200, 200, 200)
    
    star_map_surface = pygame.Surface((screen.get_width() - 400, screen.get_height()))  # Account for both UIs
    star_map_surface.fill(BLACK)
    
    cell_width = (screen.get_width() - 400) // star_map.width
    cell_height = screen.get_height() // star_map.height
    star_size = min(cell_width, cell_height) // 2  # Make stars larger

    GOLD = (255, 215, 0)
    
    for y in range(star_map.height):
        for x in range(star_map.width):
            if isinstance(star_map.map[y][x], Star):
                star = star_map.map[y][x]
                center_x = x * cell_width + cell_width // 2
                center_y = y * cell_height + cell_height // 2
                
                # Draw highlight rings for selected stars
                if star == selected_star:
                    pygame.draw.circle(star_map_surface, GOLD, 
                                    (center_x, center_y), 
                                    star_size + 4, 2)  # Circle for left-click
                if star == target_star:
                    # Draw triangle for right-click
                    points = [
                        (center_x, center_y - star_size - 8),
                        (center_x - star_size - 4, center_y + star_size + 4),
                        (center_x + star_size + 4, center_y + star_size + 4)
                    ]
                    pygame.draw.polygon(star_map_surface, GOLD, points, 2)
                
                # Draw the star
                if star.owner == -1:
                    pygame.draw.circle(star_map_surface, SOFT_WHITE, 
                                    (center_x, center_y), 
                                    star_size)
                else:
                    color = star.color
                    shape = star.shape
                    if shape == "circle":
                        pygame.draw.circle(star_map_surface, color, 
                                        (center_x, center_y), 
                                        star_size)
                    elif shape == "square":
                        rect_size = star_size * 2
                        pygame.draw.rect(star_map_surface, color, 
                                      (center_x - star_size, center_y - star_size,
                                       rect_size, rect_size))

    screen.blit(star_map_surface, (offset_x, 0))

# Additional game logic methods can be added as needed.