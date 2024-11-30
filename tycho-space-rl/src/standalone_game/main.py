# File: /tycho-space-rl/tycho-space-rl/src/standalone_game/main.py

import pygame
from game_logic import Game, draw_star_map

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Tycho Space RL")
    
    game = Game(map_width=50, map_height=50, seed=42, star_probability=0.1)
    clock = pygame.time.Clock()
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # game.handle_event(event)  # Uncomment if event handling is implemented
        
        # game.update()  # Uncomment if game update logic is implemented
        draw_star_map(game.star_map, screen)
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()

if __name__ == "__main__":
    main()