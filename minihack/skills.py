# Copyright (c) Facebook, Inc. and its affiliates.
from minihack import MiniHack
from minihack.base import MH_DEFAULT_OBS_KEYS
from gym.envs import registration


class MiniHackSkill(MiniHack):
    """The base class for MiniHack Skill Acquisition tasks.

    Navigation tasks have the following characteristics:

    - The full action space is used.
    - Yes/No questions are enabled, but the menu-selection actions are disabled
      by default.
    - The character is set to a neutral human male caveman.
    - Maximum episode limit defaults to 250 (can be overriden via the
      `max_episode_steps` argument)
    - The default goal is to reach the stair down. This can be changed using
      a reward manager.
    - Auto-pick is disabled by default.
    - Inventory strings and corresponding letter are also included as part of
      the agent observations.
    """

    def __init__(
        self,
        *args,
        des_file,
        **kwargs,
    ):
        # Autopickup off by defautlt
        kwargs["autopickup"] = kwargs.pop("autopickup", False)
        # Allowing one-letter menu questions
        kwargs["allow_all_yn_questions"] = kwargs.pop(
            "allow_all_yn_questions", True
        )
        # Perform know steps
        kwargs["allow_all_modes"] = kwargs.pop("allow_all_modes", False)
        # Play with Caveman character by default
        kwargs["character"] = kwargs.pop("character", "cav-hum-new-mal")
        # Default episode limit
        kwargs["max_episode_steps"] = kwargs.pop("max_episode_steps", 250)

        default_keys = MH_DEFAULT_OBS_KEYS + [
            "inv_strs",
            "inv_letters",
        ]
        kwargs["observation_keys"] = kwargs.pop(
            "observation_keys", default_keys
        )
        super().__init__(*args, des_file=des_file, **kwargs)


registration.register(
    id="MiniHack-Skill-Custom-v0",
    entry_point="minihack.skills:MiniHackSkill",
)
