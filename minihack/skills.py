# Copyright (c) Facebook, Inc. and its affiliates.
from minihack import MiniHack


class MiniHackSkill(MiniHack):
    """Base environment skill acquisition tasks."""

    def __init__(
        self,
        *args,
        des_file,
        reward_manager=None,
        **kwargs,
    ):
        """If reward_manager == None, the goal is to reach the staircase."""
        # Autopickup off by defautlt
        kwargs["autopickup"] = kwargs.pop("autopickup", False)
        # Allowing one-letter menu questions
        kwargs["allow_all_yn_questions"] = kwargs.pop("allow_all_yn_questions", True)
        # Perform know steps
        kwargs["allow_all_modes"] = kwargs.pop("allow_all_modes", False)
        # Play with Caveman character by default
        kwargs["character"] = kwargs.pop("character", "cav-hum-new-mal")
        # Default episode limit
        kwargs["max_episode_steps"] = kwargs.pop("max_episode_steps", 250)

        default_keys = [
            "chars_crop",
            "colors_crop",
            "screen_descriptions_crop",
            "message",
            "inv_strs",
            "inv_letters",
        ]
        kwargs["observation_keys"] = kwargs.pop("observation_keys", default_keys)
        super().__init__(
            *args, des_file=des_file, reward_manager=reward_manager, **kwargs
        )
