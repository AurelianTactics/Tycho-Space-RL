import numpy as np
import gymnasium as gym
from gymnasium import spaces

class TychoSpaceEnv(gym.Env):
    metadata = {"render_modes": ["human", "rgb_array"], "render_fps": 4}

    def __init__(self, render_mode=None):
        super().__init__()
        self.size = 5  # Example size, can be adjusted
        self.window_size = 512  # Example window size for rendering

        # Define action and observation space
        self.action_space = spaces.Discrete(4)  # Example: 4 possible actions
        self.observation_space = spaces.Dict({
            "player1": spaces.Box(0, self.size - 1, shape=(2,), dtype=int),
            "player2": spaces.Box(0, self.size - 1, shape=(2,), dtype=int),
            "stars": spaces.Box(0, self.size - 1, shape=(self.size, self.size), dtype=int)
        })

        self._player1_location = np.array([0, 0], dtype=int)
        self._player2_location = np.array([self.size - 1, self.size - 1], dtype=int)
        self._stars = np.zeros((self.size, self.size), dtype=int)

        self.render_mode = render_mode
        self.window = None
        self.clock = None

    def _get_obs(self):
        return {
            "player1": self._player1_location,
            "player2": self._player2_location,
            "stars": self._stars
        }

    def _get_info(self):
        return {
            "player1_stars": np.sum(self._stars == 1),
            "player2_stars": np.sum(self._stars == 2)
        }

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        self._player1_location = np.array([0, 0], dtype=int)
        self._player2_location = np.array([self.size - 1, self.size - 1], dtype=int)
        self._stars = np.zeros((self.size, self.size), dtype=int)
        self._stars[0, 0] = 1
        self._stars[self.size - 1, self.size - 1] = 2

        observation = self._get_obs()
        info = self._get_info()

        if self.render_mode == "human":
            self.render()

        return observation, info

    def step(self, action):
        # Example action handling
        if action == 0:  # Move right
            self._player1_location[0] = min(self.size - 1, self._player1_location[0] + 1)
        elif action == 1:  # Move up
            self._player1_location[1] = min(self.size - 1, self._player1_location[1] + 1)
        elif action == 2:  # Move left
            self._player1_location[0] = max(0, self._player1_location[0] - 1)
        elif action == 3:  # Move down
            self._player1_location[1] = max(0, self._player1_location[1] - 1)

        terminated = np.array_equal(self._player1_location, self._player2_location)
        reward = 1 if terminated else 0
        observation = self._get_obs()
        info = self._get_info()

        if self.render_mode == "human":
            self.render()

        return observation, reward, terminated, False, info

    def render(self):
        if self.render_mode == "rgb_array":
            return self._render_frame()
        elif self.render_mode == "human":
            self._render_frame()

    def _render_frame(self):
        if self.window is None and self.render_mode == "human":
            import pygame
            pygame.init()
            self.window = pygame.display.set_mode((self.window_size, self.window_size))
        if self.clock is None and self.render_mode == "human":
            import pygame
            self.clock = pygame.time.Clock()

        import pygame
        canvas = pygame.Surface((self.window_size, self.window_size))
        canvas.fill((255, 255, 255))
        pix_square_size = self.window_size / self.size

        # Draw stars
        for x in range(self.size):
            for y in range(self.size):
                if self._stars[x, y] == 1:
                    pygame.draw.circle(canvas, (0, 0, 255), (int((x + 0.5) * pix_square_size), int((y + 0.5) * pix_square_size)), int(pix_square_size / 3))
                elif self._stars[x, y] == 2:
                    pygame.draw.circle(canvas, (255, 0, 0), (int((x + 0.5) * pix_square_size), int((y + 0.5) * pix_square_size)), int(pix_square_size / 3))

        # Draw players
        pygame.draw.circle(canvas, (0, 255, 0), (int((self._player1_location[0] + 0.5) * pix_square_size), int((self._player1_location[1] + 0.5) * pix_square_size)), int(pix_square_size / 3))
        pygame.draw.circle(canvas, (255, 255, 0), (int((self._player2_location[0] + 0.5) * pix_square_size), int((self._player2_location[1] + 0.5) * pix_square_size)), int(pix_square_size / 3))

        if self.render_mode == "human":
            self.window.blit(canvas, canvas.get_rect())
            pygame.display.flip()
            self.clock.tick(self.metadata["render_fps"])
        elif self.render_mode == "rgb_array":
            return np.transpose(np.array(pygame.surfarray.pixels3d(canvas)), axes=(1, 0, 2))

    def close(self):
        if self.window is not None:
            import pygame
            pygame.display.quit()
            pygame.quit()
            self.window = None
            self.clock = None