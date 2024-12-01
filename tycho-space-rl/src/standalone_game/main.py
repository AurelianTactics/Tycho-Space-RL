# File: /tycho-space-rl/tycho-space-rl/src/standalone_game/main.py

import pygame
from game_logic import Game, draw_star_map, Star, show_star_info

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Tycho Space RL")
    
    game = Game(map_width=50, map_height=50, seed=42, star_probability=0.1, max_stars=20)
    clock = pygame.time.Clock()
    
    running = True
    show_info = False
    selected_star = None

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if show_info:
                    show_info = False
                else:
                    x, y = event.pos
                    cell_width = screen.get_width() // game.star_map.width
                    cell_height = screen.get_height() // game.star_map.height
                    grid_x = x // cell_width
                    grid_y = y // cell_height
                    if isinstance(game.star_map.map[grid_y][grid_x], Star):
                        selected_star = game.star_map.map[grid_y][grid_x]
                        show_info = True

        draw_star_map(game.star_map, screen)
        
        if show_info and selected_star:
            show_star_info(screen, selected_star)
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()

if __name__ == "__main__":
    main()