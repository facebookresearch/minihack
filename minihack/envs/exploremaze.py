# Copyright (c) Facebook, Inc. and its affiliates.
from gym.envs import registration
from minihack import MiniHackNavigation
from minihack.envs.corridor import NAVIGATE_ACTIONS
from minihack.reward_manager import RewardManager
from nle.nethack import Command

EAT_ACTION = Command.EAT
ACTIONS = tuple(list(NAVIGATE_ACTIONS) + [EAT_ACTION])


def stairs_reward_function(env, previous_observation, action, observation):
    # Agent is on stairs down
    if observation[env._internal_index][4]:
        return 1
    return 0


class MiniHackExploreMaze(MiniHackNavigation):
    """Environment for a memory challenge."""

    def __init__(self, *args, des_file, **kwargs):
        kwargs["max_episode_steps"] = kwargs.pop("max_episode_steps", 500)
        kwargs["actions"] = ACTIONS
        kwargs["allow_all_yn_questions"] = True
        reward_manager = RewardManager()
        reward_manager.add_eat_event(
            "apple",
            reward=0.5,
            repeatable=True,
            terminal_required=False,
            terminal_sufficient=False,
        )
        # Will never be achieved, but insures the environment keeps running
        reward_manager.add_message_event(
            ["Mission Complete."], terminal_required=True, terminal_sufficient=True
        )
        reward_manager.add_custom_reward_fn(stairs_reward_function)
        super().__init__(
            *args,
            des_file=des_file,
            reward_manager=reward_manager,
            **kwargs,
        )


class MiniHackExploreMazeEasy(MiniHackExploreMaze):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, des_file="exploremazeeasy.des", **kwargs)


class MiniHackExploreMazeHard(MiniHackExploreMaze):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, des_file="exploremazehard.des", **kwargs)


class MiniHackExploreMazeEasyMapped(MiniHackExploreMaze):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, des_file="exploremazeeasy_premapped.des", **kwargs)


class MiniHackExploreMazeHardMapped(MiniHackExploreMaze):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, des_file="exploremazehard_premapped.des", **kwargs)


registration.register(
    id="MiniHack-ExploreMaze-Easy-v0",
    entry_point="minihack.envs.exploremaze:MiniHackExploreMazeEasy",
)
registration.register(
    id="MiniHack-ExploreMaze-Hard-v0",
    entry_point="minihack.envs.exploremaze:MiniHackExploreMazeHard",
)
registration.register(
    id="MiniHack-ExploreMaze-Easy-Mapped-v0",
    entry_point="minihack.envs.exploremaze:MiniHackExploreMazeEasyMapped",
)
registration.register(
    id="MiniHack-ExploreMaze-Hard-Mapped-v0",
    entry_point="minihack.envs.exploremaze:MiniHackExploreMazeHardMapped",
)
