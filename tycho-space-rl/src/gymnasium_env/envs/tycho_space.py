from gymnasium import Env, spaces
import numpy as np

class TychoSpaceEnv(Env):
    metadata = {"render_modes": ["human", "rgb_array"], "render_fps": 30}

    def __init__(self, render_mode=None):
        super().__init__()
        self.render_mode = render_mode
        self.action_space = spaces.Discrete(4)  # Example: 0=up, 1=down, 2=left, 3=right
        self.observation_space = spaces.Box(low=0, high=10, shape=(2,), dtype=np.float32)  # Example observation space
        self.state = None

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        self.state = np.random.randint(0, 10, size=(2,))
        return self.state, {}

    def step(self, action):
        if action == 0:  # up
            self.state[1] += 1
        elif action == 1:  # down
            self.state[1] -= 1
        elif action == 2:  # left
            self.state[0] -= 1
        elif action == 3:  # right
            self.state[0] += 1

        done = bool(np.any(self.state < 0) or np.any(self.state > 10))  # Example termination condition
        reward = 1.0 if not done else -1.0
        info = {}

        return self.state, reward, done, False, info

    def render(self):
        pass  # Implement rendering logic here

    def close(self):
        pass  # Implement cleanup logic here