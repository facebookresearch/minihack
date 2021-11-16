# Copyright (c) Facebook, Inc. and its affiliates.
from minihack import MiniHackNavigation
from minihack.level_generator import LevelGenerator
from minihack.envs import register

DUNGEON_SHAPE = (76, 21)


class MiniHackMazeWalk(MiniHackNavigation):
    """Environment for "mazewalk" task."""

    def __init__(self, *args, w, h, premapped, **kwargs):
        kwargs["max_episode_steps"] = kwargs.pop("max_episode_steps", 1000)
        if premapped:
            flags = ("hardfloor", "premapped")
        else:
            flags = ("hardfloor",)

        if (w, h) != DUNGEON_SHAPE:
            # Fill the level with concrete walls " " surrounded by regular walls
            w, h = w + 2, h + 2
            lvl_gen = LevelGenerator(w=w, h=h, flags=flags)
            lvl_gen.fill_terrain("rect", "-", 0, 0, w - 1, h - 1)
            lvl_gen.fill_terrain("fillrect", " ", 1, 1, w - 2, h - 2)
        else:
            lvl_gen = LevelGenerator(w=w, h=h, fill=" ", flags=flags)

        lvl_gen.add_mazewalk()
        lvl_gen.add_stair_down()

        super().__init__(*args, des_file=lvl_gen.get_des(), **kwargs)


class MiniHackMazeWalk9x9(MiniHackMazeWalk):
    def __init__(self, *args, **kwargs):
        kwargs["max_episode_steps"] = kwargs.pop("max_episode_steps", 200)
        super().__init__(*args, w=9, h=9, premapped=False, **kwargs)


class MiniHackMazeWalk9x9Premapped(MiniHackMazeWalk):
    def __init__(self, *args, **kwargs):
        kwargs["max_episode_steps"] = kwargs.pop("max_episode_steps", 200)
        super().__init__(*args, w=9, h=9, premapped=True, **kwargs)


class MiniHackMazeWalk15x15(MiniHackMazeWalk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, w=15, h=15, premapped=False, **kwargs)


class MiniHackMazeWalk15x15Premapped(MiniHackMazeWalk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, w=15, h=15, premapped=True, **kwargs)


class MiniHackMazeWalk45x19(MiniHackMazeWalk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, w=45, h=19, premapped=False, **kwargs)


class MiniHackMazeWalk45x19Premapped(MiniHackMazeWalk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, w=45, h=19, premapped=True, **kwargs)


register(
    id="MiniHack-MazeWalk-9x9-v0",
    entry_point="minihack.envs.mazewalk:MiniHackMazeWalk9x9",
)
register(
    id="MiniHack-MazeWalk-Mapped-9x9-v0",
    entry_point="minihack.envs.mazewalk:MiniHackMazeWalk9x9Premapped",
)
register(
    id="MiniHack-MazeWalk-15x15-v0",
    entry_point="minihack.envs.mazewalk:MiniHackMazeWalk15x15",
)
register(
    id="MiniHack-MazeWalk-Mapped-15x15-v0",
    entry_point="minihack.envs.mazewalk:MiniHackMazeWalk15x15Premapped",
)
register(
    id="MiniHack-MazeWalk-45x19-v0",
    entry_point="minihack.envs.mazewalk:MiniHackMazeWalk45x19",
)
register(
    id="MiniHack-MazeWalk-Mapped-45x19-v0",
    entry_point="minihack.envs.mazewalk:MiniHackMazeWalk45x19Premapped",
)
