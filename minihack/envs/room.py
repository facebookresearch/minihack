# Copyright (c) Facebook, Inc. and its affiliates.
from minihack import MiniHackNavigation
from minihack import LevelGenerator
from gym.envs import registration


class MiniHackRoom(MiniHackNavigation):
    """Environment for "empty" task."""

    def __init__(
        self,
        *args,
        size=5,
        random=True,
        n_monster=0,
        n_trap=0,
        lit=True,
        **kwargs
    ):
        kwargs["max_episode_steps"] = kwargs.pop(
            "max_episode_steps", size * 20
        )

        lvl_gen = LevelGenerator(w=size, h=size, lit=lit)
        if random:
            lvl_gen.add_stair_down()
        else:
            lvl_gen.add_stair_down((size - 1, size - 1))
            lvl_gen.add_stair_up((0, 0))

        for _ in range(n_monster):
            lvl_gen.add_monster()

        for _ in range(n_trap):
            lvl_gen.add_trap()

        super().__init__(*args, des_file=lvl_gen.get_des(), **kwargs)


class MiniHackRoom5x5(MiniHackRoom):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, size=5, random=False, **kwargs)


class MiniHackRoom5x5Random(MiniHackRoom):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, size=5, random=True, **kwargs)


class MiniHackRoom5x5Dark(MiniHackRoom):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, size=5, random=True, lit=False, **kwargs)


class MiniHackRoom5x5Monster(MiniHackRoom):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, size=5, random=True, n_monster=1, **kwargs)


class MiniHackRoom5x5Trap(MiniHackRoom):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, size=5, random=True, n_trap=1, **kwargs)


class MiniHackRoom5x5Ultimate(MiniHackRoom):
    def __init__(self, *args, **kwargs):
        super().__init__(
            *args,
            size=5,
            random=True,
            lit=False,
            n_monster=1,
            n_trap=1,
            **kwargs
        )


registration.register(
    id="MiniHack-Room-5x5-v0",
    entry_point="minihack.envs.room:MiniHackRoom5x5",
)
registration.register(
    id="MiniHack-Room-Random-5x5-v0",
    entry_point="minihack.envs.room:MiniHackRoom5x5Random",
)
registration.register(
    id="MiniHack-Room-Dark-5x5-v0",
    entry_point="minihack.envs.room:MiniHackRoom5x5Dark",
)
registration.register(
    id="MiniHack-Room-Monster-5x5-v0",
    entry_point="minihack.envs.room:MiniHackRoom5x5Monster",
)
registration.register(
    id="MiniHack-Room-Trap-5x5-v0",
    entry_point="minihack.envs.room:MiniHackRoom5x5Trap",
)
registration.register(
    id="MiniHack-Room-Ultimate-5x5-v0",
    entry_point="minihack.envs.room:MiniHackRoom5x5Ultimate",
)


class MiniHackRoom15x15(MiniHackRoom):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, size=15, random=False, **kwargs)


class MiniHackRoom15x15Random(MiniHackRoom):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, size=15, random=True, **kwargs)


class MiniHackRoom15x15Dark(MiniHackRoom):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, size=15, random=True, lit=False, **kwargs)


class MiniHackRoom15x15Monster(MiniHackRoom):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, size=15, random=True, n_monster=3, **kwargs)


class MiniHackRoom15x15Trap(MiniHackRoom):
    def __init__(self, *args, **kwargs):
        super().__init__(
            *args, size=15, random=True, n_monster=0, n_trap=15, **kwargs
        )


class MiniHackRoom15x15Ultimate(MiniHackRoom):
    def __init__(self, *args, **kwargs):
        super().__init__(
            *args,
            size=15,
            random=True,
            lit=False,
            n_monster=3,
            n_trap=15,
            **kwargs
        )


registration.register(
    id="MiniHack-Room-15x15-v0",
    entry_point="minihack.envs.room:MiniHackRoom15x15",
)
registration.register(
    id="MiniHack-Room-Random-15x15-v0",
    entry_point="minihack.envs.room:MiniHackRoom15x15Random",
)
registration.register(
    id="MiniHack-Room-Dark-15x15-v0",
    entry_point="minihack.envs.room:MiniHackRoom15x15Dark",
)
registration.register(
    id="MiniHack-Room-Monster-15x15-v0",
    entry_point="minihack.envs.room:MiniHackRoom15x15Monster",
)
registration.register(
    id="MiniHack-Room-Trap-15x15-v0",
    entry_point="minihack.envs.room:MiniHackRoom15x15Trap",
)
registration.register(
    id="MiniHack-Room-Ultimate-15x15-v0",
    entry_point="minihack.envs.room:MiniHackRoom15x15Ultimate",
)
