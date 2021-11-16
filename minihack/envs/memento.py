# Copyright (c) Facebook, Inc. and its affiliates.
from minihack.envs import register
from minihack import MiniHackNavigation, RewardManager


class MiniHackMemento(MiniHackNavigation):
    """Environment for a memento challenge."""

    def __init__(self, *args, des_file, **kwargs):
        kwargs["max_episode_steps"] = kwargs.pop("max_episode_steps", 5000)
        reward_manager = RewardManager()
        reward_manager.add_message_event(
            ["squeak"],
            reward=-1,
            terminal_sufficient=True,
            terminal_required=True,
        )
        reward_manager.add_kill_event(
            "grid bug",
            reward=1,
            terminal_sufficient=True,
            terminal_required=True,
        )
        super().__init__(
            *args, des_file=des_file, reward_manager=reward_manager, **kwargs
        )


class MiniHackMementoShortF2(MiniHackMemento):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, des_file="memento_short.des", **kwargs)


class MiniHackMementoF2(MiniHackMemento):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, des_file="memento_easy.des", **kwargs)


class MiniHackMementoF4(MiniHackMemento):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, des_file="memento_hard.des", **kwargs)


register(
    id="MiniHack-Memento-Short-F2-v0",
    entry_point="minihack.envs.memento:MiniHackMementoShortF2",
)


register(
    id="MiniHack-Memento-F2-v0",
    entry_point="minihack.envs.memento:MiniHackMementoF2",
)

register(
    id="MiniHack-Memento-F4-v0",
    entry_point="minihack.envs.memento:MiniHackMementoF4",
)
