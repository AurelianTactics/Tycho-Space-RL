from gymnasium import Env, spaces
import numpy as np
from standalone_game.game_logic import TychoSpaceGame

'''
To do: be able to set the tycho space game options
'''

class TychoSpaceEnv(Env):
    metadata = {"render_modes": ["human", "rgb_array"], "render_fps": 30}

    def __init__(self, render_mode=None):
        super().__init__()
        self.render_mode = render_mode
        self.game = TychoSpaceGame(map_width=50, map_height=50, seed=1, star_probability=0.1, max_stars=10)
        num_stars = len(self.game.star_map.stars)
        self.observation_space = spaces.Box(shape=(5, num_stars), dtype=np.float32)
        #self.action_space = spaces.Discrete(4)  # Example: 0=up, 1=down, 2=left, 3=right
        self.state = None

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        self.game = TychoSpaceGame(map_width=50, map_height=50, seed=seed, star_probability=0.1, max_stars=10)
        self.state = self.game.get_observations()
        return self.state, {}

    def step(self, action):
        obs, reward, terminated, truncated, info = self.game.step(action)
        self.state = obs
        return self.state, reward, terminated, truncated, info

    def render(self):
        pass  # Implement rendering logic here

    def close(self):
        pass  # Implement cleanup logic here