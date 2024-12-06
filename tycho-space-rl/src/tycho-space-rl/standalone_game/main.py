import pygame
from game_logic import TychoSpaceGame, draw_star_map, Star, show_star_info
import random

def draw_left_ui(screen, game, selected_star, target_star, show_menu, ships_to_send="", input_active=False):
    font = pygame.font.Font(None, 36)
    ui_surface = pygame.Surface((200, screen.get_height()))
    ui_surface.fill((200, 200, 200))  # Lighter shade of gray

    # Display turn number and number of stars owned by each player
    turn_text = font.render(f"Turn: {game.turn}", True, (0, 0, 0))
    ui_surface.blit(turn_text, (10, 10))
    for i, player in enumerate(game.players):
        player_text = font.render(f"Player {i}: {sum(star.owner == i for star in game.star_map.stars)} stars", True, (0, 0, 0))
        ui_surface.blit(player_text, (10, 50 + i * 30))

    #Display selected star info with ship sending controls
    if selected_star:
        selected_text = font.render("Selected Star:", True, (0, 0, 0))
        ui_surface.blit(selected_text, (10, 150))
        show_star_info(ui_surface, selected_star, offset=(10, 180))

    # Display ship sending controls when appropriate
    if selected_star and target_star and selected_star.owner == 0:  # Only if human player (player 0) owns the star

        font_small = pygame.font.Font(None, 24)
        
        # Add ship count input box with visual feedback for active state
        input_box = pygame.Rect(10, 230, 180, 30)
        box_color = (180, 180, 255) if input_active else (240, 240, 240)  # Highlight when active
        pygame.draw.rect(ui_surface, box_color, input_box)
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
        # First show the turns to reach info if we have both stars
        if selected_star:
            turns_to_reach = game.calculate_travel_turns(selected_star, target_star)
            turns_text = font.render(f"Turns to reach: {turns_to_reach}", True, (0, 0, 0))
            ui_surface.blit(turns_text, (10, 300))
            
        # Then show target star info at a lower position
        target_text = font.render("Target Star:", True, (0, 0, 0))
        ui_surface.blit(target_text, (10, 330))
        show_star_info(ui_surface, target_star, offset=(10, 360))

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
    font = pygame.font.Font(None, 24)  # Smaller font
    ui_surface = pygame.Surface((300, screen.get_height()))  # Larger UI surface
    ui_surface.fill((200, 200, 200))  # Lighter shade of gray

    # Display log button
    log_button = pygame.Rect(10, 10, 280, 40)  # Adjust width
    pygame.draw.rect(ui_surface, (100, 100, 100), log_button)
    log_text = font.render("Log", True, (255, 255, 255))
    ui_surface.blit(log_text, (log_button.x + 110, log_button.y + 5))  # Center text

    # Display ships in flight button
    ships_button = pygame.Rect(10, 60, 280, 40)  # Adjust width
    pygame.draw.rect(ui_surface, (100, 100, 100), ships_button)
    ships_text = font.render("Ships in Flight", True, (255, 255, 255))
    ui_surface.blit(ships_text, (ships_button.x + 80, ships_button.y + 5))  # Center text

    # Display log window if log button is clicked
    if show_log:
        log_surface = pygame.Surface((280, screen.get_height() - 110))  # Adjust width
        log_surface.fill((150, 150, 150))
        log_start_y = 10
        for log in game.logs[-5:]:
            log_text = font.render(log, True, (0, 0, 0))
            log_surface.blit(log_text, (10, log_start_y))
            log_start_y += 30  # Adjust line height
        ui_surface.blit(log_surface, (10, 110))

    # Display ships in flight window if ships button is clicked
    if show_ships:
        ships_surface = pygame.Surface((280, screen.get_height() - 110))  # Adjust width
        ships_surface.fill((150, 150, 150))
        ships_start_y = 10
        sorted_ships = sorted(game.ships_in_transit, key=lambda x: x["turns_to_reach_star"])
        for ship in sorted_ships:
            ship_text = font.render(f"Player {ship['ship_owner']} -> Star {ship['star_to']} in {ship['turns_to_reach_star']} turns", True, (0, 0, 0))
            ships_surface.blit(ship_text, (10, ships_start_y))
            ships_start_y += 30  # Adjust line height
        ui_surface.blit(ships_surface, (10, 110))

    screen.blit(ui_surface, (screen.get_width() - 300, 0))  # Adjust position

def draw_game_over_popup(screen, game, winner):
    font = pygame.font.Font(None, 36)
    popup_surface = pygame.Surface((400, 300))
    popup_surface.fill((200, 200, 200))  # Lighter shade of gray
    pygame.draw.rect(popup_surface, (100, 100, 100), popup_surface.get_rect(), 2)  # Border

    # Display winner
    winner_text = font.render(f"Player {winner} wins!", True, (0, 0, 0))
    popup_surface.blit(winner_text, (100, 50))

    # Display number of turns taken
    turns_text = font.render(f"Turns taken: {game.turn}", True, (0, 0, 0))
    popup_surface.blit(turns_text, (100, 100))

    # Display number of planets the player has
    player_planets = sum(star.owner == winner for star in game.star_map.stars)
    planets_text = font.render(f"Planets owned: {player_planets}", True, (0, 0, 0))
    popup_surface.blit(planets_text, (100, 150))

    # Display total number of ships the player has
    player_ships = sum(star.total_ships for star in game.star_map.stars if star.owner == winner)
    ships_text = font.render(f"Total ships: {player_ships}", True, (0, 0, 0))
    popup_surface.blit(ships_text, (100, 200))

    # Display buttons for new game and quit game
    new_game_button = pygame.Rect(50, 250, 120, 40)
    quit_button = pygame.Rect(230, 250, 120, 40)
    pygame.draw.rect(popup_surface, (100, 100, 100), new_game_button)
    pygame.draw.rect(popup_surface, (100, 100, 100), quit_button)
    new_game_text = font.render("New Game", True, (255, 255, 255))
    quit_text = font.render("Quit", True, (255, 255, 255))
    popup_surface.blit(new_game_text, (new_game_button.x + 10, new_game_button.y + 5))
    popup_surface.blit(quit_text, (quit_button.x + 30, quit_button.y + 5))

    screen.blit(popup_surface, (screen.get_width() // 2 - 200, screen.get_height() // 2 - 150))

def main():
    pygame.init()
    screen = pygame.display.set_mode((1400, 600))
    pygame.display.set_caption("Tycho Space RL")
    
    game = TychoSpaceGame(map_width=50, map_height=50, seed=1, star_probability=0.1, max_stars=10)
    clock = pygame.time.Clock()
    
    running = True
    game_over = False
    winner = None
    selected_star = None
    target_star = None
    show_menu = False
    show_log = False
    show_ships = False
    ships_to_send = ""  # Ensure this is initialized as empty string
    input_active = False  # Add this to track if input box is selected

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if game_over:
                    # Handle game over buttons
                    if screen.get_width() // 2 - 150 <= x <= screen.get_width() // 2 - 30 and screen.get_height() // 2 + 100 <= y <= screen.get_height() // 2 + 140:
                        game = TychoSpaceGame(map_width=50, map_height=50, seed=random.randint(0, 1000), star_probability=0.1, max_stars=10)
                        game_over = False
                        winner = None
                    elif screen.get_width() // 2 + 30 <= x <= screen.get_width() // 2 + 150 and screen.get_height() // 2 + 100 <= y <= screen.get_height() // 2 + 140:
                        running = False
                else:
                    if x < 200:  # Left UI click handling
                        # Check if clicked in input box (adjusted coordinates to match actual position)
                        if selected_star and target_star and selected_star.owner == 0:
                            if 230 <= y <= 260 and 10 <= x <= 190:  # Input box coordinates
                                input_active = True
                                # Reset other UI states when input is active
                                show_menu = False
                                show_log = False
                                show_ships = False
                            elif not (230 <= y <= 260 and 10 <= x <= 190):  # Clicked outside input box
                                input_active = False
                                
                            # Handle send ships button click
                            if 270 <= y <= 300 and 10 <= x <= 190:  # Adjust coordinates as needed
                                try:
                                    num_ships = int(ships_to_send)
                                    if 0 < num_ships <= selected_star.total_ships:
                                        game.add_ships_in_transit(0, num_ships, selected_star, target_star)
                                        selected_star.total_ships -= num_ships
                                        ships_to_send = ""
                                        selected_star = None
                                        target_star = None
                                        input_active = False
                                except ValueError:
                                    pass
                        
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
                                winner = game.end_turn()
                                if winner is not None:
                                    game_over = True
                                else:
                                    game.execute_ai_turn()  # Execute AI turn after human turn ends
                                    winner = game.check_winner()
                                    if winner is not None:
                                        game_over = True
                            elif screen.get_height() - 50 <= y <= screen.get_height() - 10:  # Menu button
                                show_menu = not show_menu
                    elif x >= screen.get_width() - 300:  # Right UI click handling
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
                if input_active:  # Only handle keyboard input when input box is active
                    if event.key == pygame.K_RETURN:
                        try:
                            num_ships = int(ships_to_send)
                            if 0 < num_ships <= selected_star.total_ships:
                                game.add_ships_in_transit(0, num_ships, selected_star, target_star)
                                selected_star.total_ships -= num_ships
                                ships_to_send = ""
                                selected_star = None
                                target_star = None
                                input_active = False
                        except ValueError:
                            pass
                    elif event.key == pygame.K_BACKSPACE:
                        ships_to_send = ships_to_send[:-1]
                    elif event.unicode.isnumeric():
                        ships_to_send += event.unicode

                elif event.key == pygame.K_RETURN:  # End turn if input not active
                    winner = game.end_turn()
                    if winner is not None:
                        game_over = True
                    else:
                        game.execute_ai_turn()  # Execute AI turn after human turn ends
                        winner = game.check_winner()
                        if winner is not None:
                            game_over = True

        screen.fill((0, 0, 0))  # Clear the screen to prevent flickering
        # Change the order: draw UIs first, then star map
        draw_star_map(game.star_map, screen, offset_x=200)  # Draw star map first

        draw_left_ui(screen, game, selected_star, target_star, show_menu, ships_to_send, input_active)  # Draw UIs on top
        draw_right_ui(screen, game, show_log, show_ships)
        
        if game_over:
            draw_game_over_popup(screen, game, winner)
        
        pygame.display.flip()
        clock.tick(20)
    
    pygame.quit()

if __name__ == "__main__":
    main()