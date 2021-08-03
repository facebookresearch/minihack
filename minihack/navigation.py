# Copyright (c) Facebook, Inc. and its affiliates.

from minihack import MiniHack
from nle import nethack
from gym.envs import registration


MOVE_ACTIONS = tuple(nethack.CompassDirection)


class MiniHackNavigation(MiniHack):
    """Base class for maze-type task.

    Maze environments have
    - Restricted action space (move only by default)
    - No pet
    - One-letter menu questions are NOT allowed by default
    - Restricted observations, only glyphs by default
    - No random monster generation

    The goal is to reach the staircase.
    """

    def __init__(self, *args, des_file: str = None, **kwargs):
        # Actions space - move only by default
        kwargs["actions"] = kwargs.pop("actions", MOVE_ACTIONS)
        # Disallowing one-letter menu questions
        kwargs["allow_all_yn_questions"] = kwargs.pop(
            "allow_all_yn_questions", False
        )
        # Perform know steps
        kwargs["allow_all_modes"] = kwargs.pop("allow_all_modes", False)
        # Play with Rogue character by default
        kwargs["character"] = kwargs.pop("character", "rog-hum-cha-mal")
        # Default episode limit
        kwargs["max_episode_steps"] = kwargs.pop("max_episode_steps", 100)

        super().__init__(*args, des_file=des_file, **kwargs)


registration.register(
    id="MiniHack-Navigation-Custom-v0",
    entry_point="minihack.navigation:MiniHackNavigation",
)
