# Copyright (c) Facebook, Inc. and its affiliates.

from minihack import MiniHack
from nle import nethack
from gym.envs import registration


MOVE_ACTIONS = tuple(nethack.CompassDirection)


class MiniHackNavigation(MiniHack):
    """The base class for MiniHack Navigation tasks.

    Navigation tasks have the following characteristics:

    - Restricted action space: By default, the agent can only move towards
      eight compass directions.
    - Yes/No questions, as well as menu-selection actions are disabled by
      default.
    - The character is set to chaotic human male rogue.
    - Auto-pick is enabled by default.
    - Maximum episode limit defaults to 100 (can be overriden via the
      `max_episode_steps` argument)
    - The default goal is to reach the stair down. This can be changed using
      a reward manager.
    """

    def __init__(self, *args, des_file: str = None, **kwargs):
        # Actions space - move only by default
        kwargs["actions"] = kwargs.pop("actions", MOVE_ACTIONS)
        # Disallowing one-letter menu questions
        kwargs["allow_all_yn_questions"] = kwargs.pop(
            "allow_all_yn_questions", False
        )
        # Perform known steps
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
