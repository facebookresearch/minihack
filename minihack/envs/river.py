# Copyright (c) Facebook, Inc. and its affiliates.
from minihack import MiniHackNavigation, LevelGenerator
from minihack.envs import register


class MiniHackRiver(MiniHackNavigation):
    def __init__(self, *args, **kwargs):
        kwargs["max_episode_steps"] = kwargs.pop("max_episode_steps", 350)
        n_monster = kwargs.pop("n_monster", 0)
        n_boulder = kwargs.pop("n_boulder", 5)
        narrow = kwargs.pop("narrow", False)
        lava = kwargs.pop("lava", False)

        if narrow:
            map = """
..................WW.....
..................WW.....
..................WW.....
..................WW.....
..................WW.....
..................WW.....
..................WW.....
"""
        elif not lava:
            map = """
..................WWW....
..................WWW....
..................WWW....
..................WWW....
..................WWW....
..................WWW....
..................WWW....
"""
        else:
            map = """
..................LLL....
..................LLL....
..................WWW....
..................LLL....
..................WWW....
..................LLL....
..................LLL....
"""

        lvl_gen = LevelGenerator(map=map)
        lvl_gen.set_start_rect((0, 0), (18, 6))

        for _ in range(n_monster):
            lvl_gen.add_monster()

        lvl_gen.set_area_variable(
            "$boulder_area", type="fillrect", x1=1, y1=1, x2=18, y2=5
        )
        for _ in range(n_boulder):
            lvl_gen.add_object_area(
                "$boulder_area", name="boulder", symbol="`"
            )

        lvl_gen.add_goal_pos((24, 2))

        super().__init__(*args, des_file=lvl_gen.get_des(), **kwargs)


class MiniHackRiverMonster(MiniHackRiver):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, n_monster=5, **kwargs)


class MiniHackRiverLava(MiniHackRiver):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, lava=True, **kwargs)


class MiniHackRiverMonsterLava(MiniHackRiver):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, lava=True, n_monster=5, **kwargs)


class MiniHackRiverNarrow(MiniHackRiver):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, narrow=True, **kwargs)


register(
    id="MiniHack-River-v0",
    entry_point="minihack.envs.river:MiniHackRiver",
)

register(
    id="MiniHack-River-Monster-v0",
    entry_point="minihack.envs.river:MiniHackRiverMonster",
)

register(
    id="MiniHack-River-Lava-v0",
    entry_point="minihack.envs.river:MiniHackRiverLava",
)

register(
    id="MiniHack-River-MonsterLava-v0",
    entry_point="minihack.envs.river:MiniHackRiverMonsterLava",
)

register(
    id="MiniHack-River-Narrow-v0",
    entry_point="minihack.envs.river:MiniHackRiverNarrow",
)
