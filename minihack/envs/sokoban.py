# Copyright (c) Facebook, Inc. and its affiliates.
from minihack.envs import register
from minihack import MiniHackNavigation
from nle import nethack

MOVE_ACTIONS = tuple(nethack.CompassDirection)
NAVIGATE_ACTIONS = MOVE_ACTIONS + (
    nethack.Command.OPEN,
    nethack.Command.KICK,
    nethack.Command.SEARCH,
)


class Sokoban(MiniHackNavigation):
    def __init__(self, *args, **kwargs):
        kwargs["max_episode_steps"] = kwargs.pop("max_episode_steps", 2000)
        kwargs["actions"] = kwargs.pop("actions", NAVIGATE_ACTIONS)
        super().__init__(*args, **kwargs)


class MiniHackSokoban1a(Sokoban):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, des_file="soko1a.des", **kwargs)


class MiniHackSokoban1b(Sokoban):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, des_file="soko1b.des", **kwargs)


class MiniHackSokoban2a(Sokoban):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, des_file="soko2a.des", **kwargs)


class MiniHackSokoban2b(Sokoban):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, des_file="soko2b.des", **kwargs)


class MiniHackSokoban3a(Sokoban):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, des_file="soko3a.des", **kwargs)


class MiniHackSokoban3b(Sokoban):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, des_file="soko3b.des", **kwargs)


class MiniHackSokoban4a(Sokoban):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, des_file="soko4a.des", **kwargs)


class MiniHackSokoban4b(Sokoban):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, des_file="soko4b.des", **kwargs)


register(
    id="MiniHack-Sokoban4a-v0",
    entry_point="minihack.envs.sokoban:MiniHackSokoban4a",
)
register(
    id="MiniHack-Sokoban4b-v0",
    entry_point="minihack.envs.sokoban:MiniHackSokoban4b",
)
register(
    id="MiniHack-Sokoban3a-v0",
    entry_point="minihack.envs.sokoban:MiniHackSokoban3a",
)
register(
    id="MiniHack-Sokoban3b-v0",
    entry_point="minihack.envs.sokoban:MiniHackSokoban3b",
)
register(
    id="MiniHack-Sokoban2a-v0",
    entry_point="minihack.envs.sokoban:MiniHackSokoban2a",
)
register(
    id="MiniHack-Sokoban2b-v0",
    entry_point="minihack.envs.sokoban:MiniHackSokoban2b",
)
register(
    id="MiniHack-Sokoban1a-v0",
    entry_point="minihack.envs.sokoban:MiniHackSokoban1a",
)
register(
    id="MiniHack-Sokoban1b-v0",
    entry_point="minihack.envs.sokoban:MiniHackSokoban1b",
)
