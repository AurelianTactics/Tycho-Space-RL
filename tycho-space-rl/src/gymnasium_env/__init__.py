# src/gymnasium_env/__init__.py

from gymnasium.envs.registration import register

register(
    id="gymnasium_env/TychoSpace-v0",
    entry_point="gymnasium_env.envs.tycho_space:TychoSpaceEnv",
)