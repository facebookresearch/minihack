# Copyright (c) Facebook, Inc. and its affiliates.
from minihack import MiniHackNavigation, LevelGenerator
from minihack.envs import register


class MiniHackLabyrinth(MiniHackNavigation):
    def __init__(self, *args, **kwargs):
        map = """
-------------------------------------
|.................|.|...............|
|.|-------------|.|.|.------------|.|
|.|.............|.|.|.............|.|
|.|.|----------.|.|.|------------.|.|
|.|.|...........|.|.............|.|.|
|.|.|.|----------.|-----------|.|.|.|
|.|.|.|...........|.......|...|.|.|.|
|.|.|.|.|----------------.|.|.|.|.|.|
|.|.|.|.|.................|.|.|.|.|.|
|.|.|.|.|.-----------------.|.|.|.|.|
|.|.|.|.|...................|.|.|.|.|
|.|.|.|.|--------------------.|.|.|.|
|.|.|.|.......................|.|.|.|
|.|.|.|-----------------------|.|.|.|
|.|.|...........................|.|.|
|.|.|---------------------------|.|.|
|.|...............................|.|
|.|-------------------------------|.|
|...................................|
-------------------------------------
"""
        lvl_gen = LevelGenerator(map=map, lit=True)
        lvl_gen.set_start_pos((19, 1))
        lvl_gen.add_goal_pos((19, 7))

        des_file = lvl_gen.get_des()
        kwargs["max_episode_steps"] = kwargs.pop("max_episode_steps", 1000)

        super().__init__(
            *args,
            des_file=des_file,
            **kwargs,
        )


class MiniHackLabyrinthSmall(MiniHackNavigation):
    def __init__(self, *args, **kwargs):
        map = """
--------------------
|.......|.|........|
|.-----.|.|.-----|.|
|.|...|.|.|......|.|
|.|.|.|.|.|-----.|.|
|.|.|...|....|.|.|.|
|.|.--------.|.|.|.|
|.|..........|...|.|
|.|--------------|.|
|..................|
--------------------
"""
        lvl_gen = LevelGenerator(map=map, lit=True)
        lvl_gen.set_start_pos((9, 1))
        lvl_gen.add_goal_pos((14, 5))

        des_file = lvl_gen.get_des()
        kwargs["max_episode_steps"] = kwargs.pop("max_episode_steps", 400)

        super().__init__(
            *args,
            des_file=des_file,
            **kwargs,
        )


register(
    id="MiniHack-Labyrinth-Big-v0",
    entry_point="minihack.envs.lab:MiniHackLabyrinth",
)

register(
    id="MiniHack-Labyrinth-Small-v0",
    entry_point="minihack.envs.lab:MiniHackLabyrinthSmall",
)
