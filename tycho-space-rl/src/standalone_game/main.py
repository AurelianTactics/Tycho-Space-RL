import pygame
from game_logic import Game, draw_star_map, Star, show_star_info
import random

def draw_ui(screen, game, selected_star, target_star, show_menu):
    font = pygame.font.Font(None, 36)
    ui_surface = pygame.Surface((200, screen.get_height()))
    ui_surface.fill((200, 200, 200))  # Lighter shade of gray

    # Display turn number and number of stars owned by each player
    turn_text = font.render(f"Turn: {game.turn}", True, (0, 0, 0))
    ui_surface.blit(turn_text, (10, 10))
    for i, player in enumerate(game.players):
        player_text = font.render(f"Player {i}: {sum(star.owner == i for star in game.star_map.stars)} stars", True, (0, 0, 0))
        ui_surface.blit(player_text, (10, 50 + i * 30))

    # Display selected star info
    if selected_star:
        selected_text = font.render("Selected Star:", True, (0, 0, 0))
        ui_surface.blit(selected_text, (10, 150))
        show_star_info(ui_surface, selected_star, offset=(10, 180))

    # Display target star info
    if target_star:
        target_text = font.render("Target Star:", True, (0, 0, 0))
        ui_surface.blit(target_text, (10, 300))
        show_star_info(ui_surface, target_star, offset=(10, 330))

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

def main():
    pygame.init()
    screen = pygame.display.set_mode((1000, 600))
    pygame.display.set_caption("Tycho Space RL")
    
    game = Game(map_width=50, map_height=50, seed=42, star_probability=0.1, max_stars=20)
    clock = pygame.time.Clock()
    
    running = True
    selected_star = None
    target_star = None
    show_menu = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if x < 200:
                    if show_menu:
                        if 10 <= y <= 50:
                            game = Game(map_width=50, map_height=50, seed=random.randint(0, 1000), star_probability=0.1, max_stars=20)
                            selected_star = None
                            target_star = None
                            show_menu = False
                        elif 60 <= y <= 100:
                            running = False
                    elif 10 <= y <= 50:
                        show_menu = not show_menu
                    elif 10 <= y <= 100:
                        game.end_turn()
                else:
                    cell_width = (screen.get_width() - 200) // game.star_map.width
                    cell_height = screen.get_height() // game.star_map.height
                    grid_x = (x - 200) // cell_width
                    grid_y = y // cell_height
                    if isinstance(game.star_map.map[grid_y][grid_x], Star):
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
                    game.end_turn()

        screen.fill((0, 0, 0))  # Clear the screen to prevent flickering
        draw_star_map(game.star_map, screen, offset_x=200)
        draw_ui(screen, game, selected_star, target_star, show_menu)
        
        pygame.display.flip()
        clock.tick(20)
    
    pygame.quit()

if __name__ == "__main__":
    main()