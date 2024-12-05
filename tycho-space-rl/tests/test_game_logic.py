import pytest
import sys
import os
from src.standalone_game.game_logic import Star, StarMap, TychoSpaceGame

def test_star_initialization():
    star = Star(index=0, x=10, y=20, owner=1, total_ships=50)
    assert star.index == 0
    assert star.x == 10
    assert star.y == 20
    assert star.owner == 1
    assert star.total_ships == 50

def test_star_distance():
    star1 = Star(index=0, x=0, y=0)
    star2 = Star(index=1, x=3, y=4)
    assert star1.distance_to(star2) == 5.0

def test_star_map_initialization():
    star_map = StarMap(map_width=10, map_height=10, seed=42, star_probability=1.0)
    assert len(star_map.stars) > 0
    assert star_map.width == 10
    assert star_map.height == 10

def test_tycho_space_game_initialization():
    game = TychoSpaceGame(map_width=10, map_height=10, num_players=2)
    assert len(game.players) == 2
    assert game.num_players == 2
    assert game.turn == 0

def test_add_ships_in_transit():
    game = TychoSpaceGame(map_width=10, map_height=10, num_players=2)
    star_from = game.star_map.stars[0]
    star_to = game.star_map.stars[1]
    game.add_ships_in_transit(ship_owner=0, number_of_ships=10, star_from=star_from, star_to=star_to)
    assert len(game.ships_in_transit) == 1
    assert game.ships_in_transit[0]["number_of_ships"] == 10

def test_update_ships_in_transit():
    game = TychoSpaceGame(map_width=10, map_height=10, num_players=2)
    star_from = game.star_map.stars[0]
    star_to = game.star_map.stars[1]
    game.add_ships_in_transit(ship_owner=0, number_of_ships=10, star_from=star_from, star_to=star_to)
    game.update_ships_in_transit()
    assert game.ships_in_transit[0]["turns_to_reach_star"] == game.calculate_travel_turns(star_from, star_to) - 1

def test_check_victory_conditions():
    game = TychoSpaceGame(map_width=10, map_height=10, num_players=2)
    game.star_map.stars[0].owner = 0
    game.star_map.stars[1].owner = 0
    game.star_map.stars[2].owner = 1
    assert game.check_victory_conditions() is None
    game.star_map.stars[2].owner = 0
    assert game.check_victory_conditions() == 0

def test_increment_turn():
    game = TychoSpaceGame(map_width=10, map_height=10, num_players=2)
    game.increment_turn()
    assert game.turn == 1

def test_end_turn():
    game = TychoSpaceGame(map_width=10, map_height=10, num_players=2)
    game.end_turn()
    assert game.turn == 1
    assert len(game.logs) == 1

def test_star_battle():
    game = TychoSpaceGame(map_width=10, map_height=10, num_players=2)
    star_from = game.star_map.stars[0]
    star_to = game.star_map.stars[1]
    star_to.owner = 1
    star_to.total_ships = 5
    game.add_ships_in_transit(ship_owner=0, number_of_ships=10, star_from=star_from, star_to=star_to)
    game.update_ships_in_transit()
    game.star_battle(game.ships_in_transit[0])
    assert star_to.owner == 0
    assert star_to.total_ships == 5

def test_generate_players():
    game = TychoSpaceGame(map_width=10, map_height=10, num_players=2)
    game.generate_players()
    assert len(game.players) == 2
    assert game.players[0].owner == 0
    assert game.players[1].owner == 1