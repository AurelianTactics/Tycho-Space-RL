import pygame
from game_logic import TychoSpaceGame, draw_star_map, Star, show_star_info
import random

def draw_left_ui(screen, game, selected_star, target_star, show_menu, ships_to_send=""):
    font = pygame.font.Font(None, 36)
    ui_surface = pygame.Surface((200, screen.get_height()))
    ui_surface.fill((200, 200, 200))  # Lighter shade of gray

    # Display turn number and number of stars owned by each player
    turn_text = font.render(f"Turn: {game.turn}", True, (0, 0, 0))
    ui_surface.blit(turn_text, (10, 10))
    for i, player in enumerate(game.players):
        player_text = font.render(f"Player {i}: {sum(star.owner == i for star in game.star_map.stars)} stars", True, (0, 0, 0))
        ui_surface.blit(player_text, (10, 50 + i * 30))

    # Display selected star info with ship sending controls
    if selected_star:
        selected_text = font.render("Selected Star:", True, (0, 0, 0))
        ui_surface.blit(selected_text, (10, 150))
        show_star_info(ui_surface, selected_star, offset=(10, 180))

        # Add ship sending controls if we have both stars selected and own the source star
        if target_star and selected_star.owner >= 0:
            ships_to_send = getattr(selected_star, 'ships_to_send', 0)
            
            # Add +/- buttons and ship count
            font_small = pygame.font.Font(None, 24)
            minus_btn = pygame.Rect(10, 230, 20, 20)
            plus_btn = pygame.Rect(80, 230, 20, 20)
            pygame.draw.rect(ui_surface, (100, 100, 100), minus_btn)
            pygame.draw.rect(ui_surface, (100, 100, 100), plus_btn)
            ui_surface.blit(font_small.render("-", True, (255, 255, 255)), (15, 230))
            ui_surface.blit(font_small.render("+", True, (255, 255, 255)), (85, 230))
            ui_surface.blit(font_small.render(f"Ships: {ships_to_send}", True, (0, 0, 0)), (35, 230))

            # Add send ships button if we can send ships
            if 0 < ships_to_send <= selected_star.total_ships:
                send_btn = pygame.Rect(10, 260, 100, 30)
                pygame.draw.rect(ui_surface, (100, 100, 100), send_btn)
                ui_surface.blit(font_small.render("Send Ships", True, (255, 255, 255)), (15, 265))

    # Display ship sending controls when appropriate
    if selected_star and target_star and selected_star.owner == 0:  # Only if human player (player 0) owns the star
        font_small = pygame.font.Font(None, 24)
        
        # Add ship count input box
        input_box = pygame.Rect(10, 230, 180, 30)
        pygame.draw.rect(ui_surface, (240, 240, 240), input_box)  # Light background
        pygame.draw.rect(ui_surface, (100, 100, 100), input_box, 2)  # Border
        
        # Show current input or placeholder
        text = font_small.render(f"Ships to send: {ships_to_send}", True, (0, 0, 0))
        ui_surface.blit(text, (15, 235))

        # Add send ships button if we have a valid number
        try:
            num_ships = int(ships_to_send) if ships_to_send else 0
            if 0 < num_ships <= selected_star.total_ships:
                send_btn = pygame.Rect(10, 270, 180, 30)
                pygame.draw.rect(ui_surface, (0, 150, 0), send_btn)
                send_text = font_small.render(f"Send {num_ships} Ships", True, (255, 255, 255))
                ui_surface.blit(send_text, (45, 275))
        except ValueError:
            pass

    # Display target star info
    if target_star:
        target_text = font.render("Target Star:", True, (0, 0, 0))
        ui_surface.blit(target_text, (10, 300))
        show_star_info(ui_surface, target_star, offset=(10, 330))

    if selected_star and target_star:
        turns_to_reach = game.calculate_travel_turns(selected_star, target_star)
        turns_text = font.render(f"Turns to reach: {turns_to_reach}", True, (0, 0, 0))
        ui_surface.blit(turns_text, (10, 300))

    # Display end turn button
    end_turn_button = pygame.Rect(10, screen.get_height() - 100, 180, 40)
    pygame.draw.rect(ui_surface, (100, 100, 100), end_turn_button)
    end_turn_text = font.render("End Turn", True, (255, 255, 255))
    ui_surface.blit(end_turn_text, (end_turn_button.x + 30, end_turn_button.y + 5))

    # Display menu button
    menu_button = pygame.Rect(10, screen.get_height() - 50, 180, 40)
    pygame.draw.rect(ui_surface, (100, 100, 100), menu_button)
    menu_text = font.render("Menu", True, (255, 255, 255))
    ui_surface.blit(menu_text, (menu_button.x + 50, menu_button.y + 5))

    # Display menu options if menu is open
    if show_menu:
        new_game_button = pygame.Rect(10, screen.get_height() - 150, 180, 40)
        quit_button = pygame.Rect(10, screen.get_height() - 200, 180, 40)
        pygame.draw.rect(ui_surface, (100, 100, 100), new_game_button)
        pygame.draw.rect(ui_surface, (100, 100, 100), quit_button)
        new_game_text = font.render("New Game", True, (255, 255, 255))
        quit_text = font.render("Quit", True, (255, 255, 255))
        ui_surface.blit(new_game_text, (new_game_button.x + 20, new_game_button.y + 5))
        ui_surface.blit(quit_text, (quit_button.x + 50, quit_button.y + 5))

    screen.blit(ui_surface, (0, 0))

def draw_right_ui(screen, game, show_log, show_ships):
    font = pygame.font.Font(None, 36)
    ui_surface = pygame.Surface((200, screen.get_height()))
    ui_surface.fill((200, 200, 200))  # Lighter shade of gray

    # Display log button
    log_button = pygame.Rect(10, 10, 180, 40)
    pygame.draw.rect(ui_surface, (100, 100, 100), log_button)
    log_text = font.render("Log", True, (255, 255, 255))
    ui_surface.blit(log_text, (log_button.x + 60, log_button.y + 5))

    # Display ships in flight button
    ships_button = pygame.Rect(10, 60, 180, 40)
    pygame.draw.rect(ui_surface, (100, 100, 100), ships_button)
    ships_text = font.render("Ships in Flight", True, (255, 255, 255))
    ui_surface.blit(ships_text, (ships_button.x + 20, ships_button.y + 5))

    # Display log window if log button is clicked
    if show_log:
        log_surface = pygame.Surface((200, screen.get_height() - 110))
        log_surface.fill((150, 150, 150))
        log_start_y = 10
        for log in game.logs[-5:]:
            log_text = font.render(log, True, (0, 0, 0))
            log_surface.blit(log_text, (10, log_start_y))
            log_start_y += 40
        ui_surface.blit(log_surface, (0, 110))

    # Display ships in flight window if ships button is clicked
    if show_ships:
        ships_surface = pygame.Surface((200, screen.get_height() - 110))
        ships_surface.fill((150, 150, 150))
        ships_start_y = 10
        sorted_ships = sorted(game.ships_in_transit, key=lambda x: x["turns_to_reach_star"])
        for ship in sorted_ships:
            ship_text = font.render(f"Player {ship['ship_owner']} -> Star {ship['star_to']} in {ship['turns_to_reach_star']} turns", True, (0, 0, 0))
            ships_surface.blit(ship_text, (10, ships_start_y))
            ships_start_y += 40
        ui_surface.blit(ships_surface, (0, 110))

    screen.blit(ui_surface, (screen.get_width() - 200, 0))

def main():
    pygame.init()
    screen = pygame.display.set_mode((1400, 600))
    pygame.display.set_caption("Tycho Space RL")
    
    game = TychoSpaceGame(map_width=50, map_height=50, seed=1, star_probability=0.1, max_stars=10)
    clock = pygame.time.Clock()
    
    running = True
    selected_star = None
    target_star = None
    show_menu = False
    show_log = False
    show_ships = False
    ships_to_send = ""  # Add this variable for text input

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if x < 200:  # Left UI click handling
                    if selected_star and target_star and selected_star.owner >= 0:
                        ships_to_send = getattr(selected_star, 'ships_to_send', 0)
                        
                        # Handle +/- buttons
                        if 230 <= y <= 250:
                            if 10 <= x <= 30:  # Minus button
                                selected_star.ships_to_send = max(0, ships_to_send - 1)
                            elif 80 <= x <= 100:  # Plus button
                                selected_star.ships_to_send = min(selected_star.total_ships, ships_to_send + 1)
                        
                        # Handle send ships button
                        elif 260 <= y <= 290 and 10 <= x <= 110 and 0 < ships_to_send <= selected_star.total_ships:
                            game.add_ships_in_transit(selected_star.owner, ships_to_send, selected_star, target_star)
                            selected_star.total_ships -= ships_to_send
                            selected_star.ships_to_send = 0
                            selected_star = None
                            target_star = None
                    
                    if show_menu:
                        if screen.get_height() - 200 <= y <= screen.get_height() - 160:  # Quit button
                            running = False
                        elif screen.get_height() - 150 <= y <= screen.get_height() - 110:  # New Game button
                            game = TychoSpaceGame(map_width=50, map_height=50, seed=random.randint(0, 1000), star_probability=0.1, max_stars=10)
                            selected_star = None
                            target_star = None
                            show_menu = False
                    else:
                        if screen.get_height() - 100 <= y <= screen.get_height() - 60:  # End Turn button
                            game.end_turn()
                        elif screen.get_height() - 50 <= y <= screen.get_height() - 10:  # Menu button
                            show_menu = not show_menu
                elif x >= screen.get_width() - 200:  # Right UI click handling
                    if 10 <= y <= 50:
                        show_log = not show_log
                        show_ships = False
                    elif 60 <= y <= 100:
                        show_ships = not show_ships
                        show_log = False
                else:  # Star map click handling
                    # Adjust click position to account for the left UI offset
                    adjusted_x = x - 200
                    # Calculate grid position using the map's actual dimensions
                    cell_width = (screen.get_width() - 400) // game.star_map.width
                    cell_height = screen.get_height() // game.star_map.height
                    grid_x = adjusted_x // cell_width
                    grid_y = y // cell_height
                    
                    if (0 <= grid_x < game.star_map.width and 
                        0 <= grid_y < game.star_map.height and 
                        isinstance(game.star_map.map[grid_y][grid_x], Star)):
                        if event.button == 1:
                            selected_star = game.star_map.map[grid_y][grid_x]
                        elif event.button == 3:
                            target_star = game.star_map.map[grid_y][grid_x]
                    else:
                        if event.button == 1:
                            selected_star = None
                        elif event.button == 3:
                            target_star = None
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if selected_star and target_star and selected_star.owner == 0:
                        try:
                            num_ships = int(ships_to_send)
                            if 0 < num_ships <= selected_star.total_ships:
                                game.add_ships_in_transit(0, num_ships, selected_star, target_star)
                                selected_star.total_ships -= num_ships
                                ships_to_send = ""
                                selected_star = None
                                target_star = None
                        except ValueError:
                            pass
                    else:
                        game.end_turn()
                elif event.key == pygame.K_BACKSPACE:
                    ships_to_send = ships_to_send[:-1]
                elif selected_star and target_star and selected_star.owner == 0:
                    if event.unicode.isnumeric():
                        ships_to_send += event.unicode

        screen.fill((0, 0, 0))  # Clear the screen to prevent flickering
        # Change the order: draw UIs first, then star map
        draw_star_map(game.star_map, screen, offset_x=200)  # Draw star map first
        draw_left_ui(screen, game, selected_star, target_star, show_menu, ships_to_send)  # Draw UIs on top
        draw_right_ui(screen, game, show_log, show_ships)
        
        pygame.display.flip()
        clock.tick(20)
    
    pygame.quit()

if __name__ == "__main__":
    main()